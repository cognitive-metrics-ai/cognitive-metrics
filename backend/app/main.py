import uuid
import datetime
import logging
from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, text, func, or_

from .database import engine, Base, get_db, SessionLocal, DATABASE_URL
from .models import Project, Proposal, NewsletterSubscriber, User, UserProject, ProjectComment
from .schemas import (
    ProjectResponse,
    ProjectCreate,
    ProjectUpdate,
    ProposalRequest,
    ProposalResponse,
    NewsletterRequest,
    NewsletterResponse,
    UserSyncRequest,
    UserResponse,
    ProjectCommentCreate,
    ProjectCommentResponse
)
from .seed import seed_initial_projects, seed_initial_users

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cognitive_metrics.api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize database tables and seed defaults."""
    logger.info("Initializing database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        # Ensure schema migrations for relational tables exist on live Neon PostgreSQL
        if engine.dialect.name == "postgresql":
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS user_id VARCHAR(128);"))
                conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS user_email VARCHAR(255);"))
                conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS is_public BOOLEAN DEFAULT true;"))
                conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS phase VARCHAR(100) DEFAULT 'Phase 1: Agentic Specification';"))
                conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS production_url VARCHAR(500);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_projects_user_id ON projects (user_id);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_project_comments_project_id ON project_comments (project_id);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_project_comments_user_id ON project_comments (user_id);"))
                conn.execute(text("ALTER TABLE proposals ADD COLUMN IF NOT EXISTS user_id VARCHAR(128);"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_proposals_user_id ON proposals (user_id);"))
                conn.commit()
        # Seed initial projects and users if empty
        with SessionLocal() as db:
            seed_initial_projects(db)
            seed_initial_users(db)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error("Database initialization error: %s", e)
    yield
    logger.info("Application shutting down.")

app = FastAPI(
    title="Cognitive Metrics API",
    description="Backend API and Neon PostgreSQL persistence layer for academic ADLC testbeds and telemetry.",
    version="1.2.0",
    lifespan=lifespan
)

# Enable CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Health Check ---
@app.get("/health")
def health(db: Session = Depends(get_db)):
    """Health check endpoint displaying service and database status."""
    is_neon = "neon.tech" in DATABASE_URL
    dialect = "Neon PostgreSQL" if is_neon else engine.dialect.name
    
    try:
        project_count = db.query(Project).count()
        db_status = "connected"
    except Exception as e:
        logger.error("Healthcheck DB query failed: %s", e)
        db_status = f"unhealthy: {str(e)}"
        project_count = 0

    return {
        "status": "ok",
        "service": "Cognitive Metrics API",
        "database": {
            "status": db_status,
            "dialect": dialect,
            "is_neon": is_neon,
            "project_records": project_count
        },
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

# --- Projects Endpoints (Neon DB) ---

def resolve_user_conditions(user_id: Optional[str], email: Optional[str], db: Session):
    """Resolve all possible project matching conditions across user_id, user_projects junction table, and email."""
    candidate_user_ids = set()
    candidate_emails = set()

    if user_id and user_id.strip():
        clean_uid = user_id.strip()
        candidate_user_ids.add(clean_uid)
        if "@" in clean_uid:
            candidate_emails.add(clean_uid.lower())

    if email and email.strip():
        candidate_emails.add(email.strip().lower())

    # Look up user in database by ID or by email
    user_rec = None
    if candidate_user_ids:
        user_rec = db.query(User).filter(User.id.in_(candidate_user_ids)).first()
    if not user_rec and candidate_emails:
        user_rec = db.query(User).filter(func.lower(User.email).in_(candidate_emails)).first()

    if user_rec:
        candidate_user_ids.add(user_rec.id)
        if user_rec.email:
            candidate_emails.add(user_rec.email.strip().lower())

    # Ensure Jeremy Lankford (Lead Architect) maps to both default ID and email
    if any(e in ["jwlankford@gmail.com", "jlankford@cognitivemetrics.org"] for e in candidate_emails) or "Jq4WTmNLN9XbtDqZsbIesLWCTTn1" in candidate_user_ids:
        candidate_user_ids.add("Jq4WTmNLN9XbtDqZsbIesLWCTTn1")
        candidate_emails.add("jwlankford@gmail.com")

    junction_project_ids = []
    if candidate_user_ids:
        junction_project_ids = [
            r[0] for r in db.query(UserProject.project_id).filter(UserProject.user_id.in_(candidate_user_ids)).all()
        ]

    conditions = []
    if candidate_user_ids:
        conditions.append(Project.user_id.in_(candidate_user_ids))
    if junction_project_ids:
        conditions.append(Project.id.in_(junction_project_ids))
    if candidate_emails:
        conditions.append(func.lower(Project.user_email).in_(candidate_emails))

    return conditions, candidate_user_ids, candidate_emails, user_rec

@app.get("/api/projects", response_model=List[ProjectResponse])
def get_projects(
    user_id: Optional[str] = Query(None, description="Filter projects tied to a specific signed user ID"),
    active_only: bool = Query(True, description="Filter only active projects"),
    db: Session = Depends(get_db)
):
    """Retrieve projects stored in the database, optionally filtered by user ID."""
    query = db.query(Project)
    if active_only:
        query = query.filter(Project.is_active == True)
    if user_id:
        conditions, _, _, _ = resolve_user_conditions(user_id, None, db)
        if conditions:
            from sqlalchemy import or_
            query = query.filter(or_(*conditions))
        else:
            return []
    return query.order_by(desc(Project.created_at)).all()

@app.get("/api/users/{user_id}/projects", response_model=List[ProjectResponse])
def get_user_projects(
    user_id: str,
    email: Optional[str] = Query(None, description="User email for cross-referencing"),
    include_shared: bool = Query(False, description="Include shared ADLC baseline testbeds if user has no assigned projects"),
    db: Session = Depends(get_db)
):
    """Retrieve all projects tied to a user at the database table level (direct ownership or junction table)."""
    from sqlalchemy import or_
    conditions, candidate_uids, candidate_emails, user_rec = resolve_user_conditions(user_id, email, db)

    if not conditions:
        return []

    user_projects = db.query(Project).filter(
        or_(*conditions),
        Project.is_active == True
    ).order_by(desc(Project.created_at)).all()

    # Auto-heal: Ensure junction records and project.user_id reflect active user
    active_uid = user_rec.id if user_rec else user_id
    if user_projects and active_uid:
        updated_links = False
        for proj in user_projects:
            if not proj.user_id:
                proj.user_id = active_uid
                updated_links = True
            link = db.query(UserProject).filter(
                UserProject.user_id == active_uid,
                UserProject.project_id == proj.id
            ).first()
            if not link:
                db.add(UserProject(user_id=active_uid, project_id=proj.id, role="lead_architect"))
                updated_links = True
        if updated_links:
            try:
                db.commit()
            except Exception as autoheal_err:
                db.rollback()
                logger.warning("Could not auto-heal user_projects link: %s", autoheal_err)

    if user_projects or not include_shared:
        return user_projects

    return []

@app.post("/api/users/sync", response_model=UserResponse)
def sync_user(payload: UserSyncRequest, db: Session = Depends(get_db)):
    """Automatically records or updates user in the database users table and associates pre-tied projects."""
    logger.info("Syncing user with PostgreSQL users table: %s (%s)", payload.id, payload.email)
    try:
        clean_email = payload.email.strip().lower() if payload.email else ""
        is_lead = clean_email in ["jwlankford@gmail.com", "jlankford@cognitivemetrics.org"]

        user = db.query(User).filter(User.id == payload.id).first()
        if not user and clean_email:
            # Check by email in case user was pre-seeded
            user = db.query(User).filter(func.lower(User.email) == clean_email).first()
            if user and user.id != payload.id:
                old_id = user.id
                new_id = payload.id
                try:
                    # Delete conflicting junction records before migrating user_id
                    db.execute(text("""
                        DELETE FROM user_projects 
                        WHERE user_id = :old_id 
                          AND project_id IN (SELECT project_id FROM user_projects WHERE user_id = :new_id)
                    """), {"old_id": old_id, "new_id": new_id})
                    db.execute(text("UPDATE user_projects SET user_id = :new_id WHERE user_id = :old_id"), {"new_id": new_id, "old_id": old_id})
                    db.execute(text("UPDATE projects SET user_id = :new_id WHERE user_id = :old_id"), {"new_id": new_id, "old_id": old_id})
                    db.execute(text("UPDATE project_comments SET user_id = :new_id WHERE user_id = :old_id"), {"new_id": new_id, "old_id": old_id})
                    db.execute(text("UPDATE proposals SET user_id = :new_id WHERE user_id = :old_id"), {"new_id": new_id, "old_id": old_id})
                    db.execute(text("UPDATE users SET id = :new_id WHERE id = :old_id"), {"new_id": new_id, "old_id": old_id})
                    db.commit()
                    user = db.query(User).filter(User.id == new_id).first()
                except Exception as id_err:
                    db.rollback()
                    logger.warning("Could not mutate primary key id directly, continuing with existing user record: %s", id_err)
                    user = db.query(User).filter(func.lower(User.email) == clean_email).first()

        if not user:
            display_name = payload.display_name
            if not display_name and clean_email:
                display_name = clean_email.split('@')[0]
            if is_lead and not display_name:
                display_name = "Jeremy Lankford"

            user = User(
                id=payload.id,
                email=clean_email,
                display_name=display_name,
                role="lead_architect" if is_lead else "researcher",
                institution=payload.institution,
                department=payload.department
            )
            db.add(user)
            logger.info("Successfully registered user in users table: %s (%s)", user.id, user.email)
        else:
            if is_lead:
                user.role = "lead_architect"
                if not user.display_name or user.display_name == user.email.split('@')[0]:
                    user.display_name = "Jeremy Lankford"
            if payload.display_name and (not user.display_name or user.display_name == user.email.split('@')[0] or is_lead):
                user.display_name = payload.display_name
            if clean_email and clean_email != user.email.lower():
                user.email = clean_email
            if payload.institution and not user.institution:
                user.institution = payload.institution
            if payload.department and not user.department:
                user.department = payload.department

        # Auto-link any projects tied to this user's email at the table level
        if clean_email:
            pre_assigned = db.query(Project).filter(func.lower(Project.user_email) == clean_email).all()
            for proj in pre_assigned:
                if not proj.user_id or proj.user_id != user.id:
                    proj.user_id = user.id
                # Also ensure junction record in user_projects table
                link = db.query(UserProject).filter(UserProject.user_id == user.id, UserProject.project_id == proj.id).first()
                if not link:
                    role = "lead_architect" if is_lead else "collaborator"
                    db.add(UserProject(user_id=user.id, project_id=proj.id, role=role))

        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        logger.error("Failed to sync user with PostgreSQL: %s", e)
        raise HTTPException(status_code=500, detail=f"Database user sync failed: {str(e)}")

@app.post("/api/user-projects", status_code=status.HTTP_201_CREATED)
def tie_user_project_at_table_level(
    user_id: str = Query(..., description="User ID"),
    project_id: str = Query(..., description="Project ID"),
    role: str = Query("lead_architect", description="Role on project"),
    db: Session = Depends(get_db)
):
    """Tie a user to a project directly in the user_projects junction table in PostgreSQL."""
    # Ensure project exists
    project = db.query(Project).filter(
        (Project.id == project_id) | (Project.slug == project_id)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")

    # Ensure user exists in users table (insert if needed)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, email=f"{user_id}@researcher.local", display_name="Researcher")
        db.add(user)
        db.flush()

    link = db.query(UserProject).filter(
        UserProject.user_id == user.id,
        UserProject.project_id == project.id
    ).first()

    if not link:
        link = UserProject(user_id=user.id, project_id=project.id, role=role)
        db.add(link)
    else:
        link.role = role

    # Also update project owner ID
    project.user_id = user.id
    db.commit()
    return {"status": "success", "message": f"Project '{project.id}' tied to user '{user.id}' at database table level."}

@app.post("/api/projects/{project_id}/assign", response_model=ProjectResponse)
def assign_project_to_user(
    project_id: str,
    user_id: str = Query(..., description="User ID to tie this project to"),
    user_email: Optional[str] = Query(None, description="Optional user email"),
    db: Session = Depends(get_db)
):
    """Tie a project to a signed user ID and record it in the database tables."""
    project = db.query(Project).filter(
        (Project.id == project_id) | (Project.slug == project_id)
    ).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found."
        )
    
    if not user_id or user_id.strip().lower() in ["unassigned", "none", "null", ""]:
        project.user_id = None
        project.user_email = None
        db.query(UserProject).filter(UserProject.project_id == project.id).delete(synchronize_session=False)
        db.commit()
        db.refresh(project)
        return project

    project.user_id = user_id
    if user_email:
        project.user_email = user_email
    else:
        project.user_email = None

    # Clean up prior junction records for this project so it binds cleanly
    db.query(UserProject).filter(UserProject.project_id == project.id).delete(synchronize_session=False)

    # Also ensure user and junction table record exist
    user = db.query(User).filter(User.id == user_id).first()
    if not user and user_email:
        user = db.query(User).filter(func.lower(User.email) == func.lower(user_email)).first()
        if not user:
            user = User(id=user_id, email=user_email, display_name=user_email.split('@')[0])
            db.add(user)
            db.flush()
    
    if user:
        link = db.query(UserProject).filter(UserProject.user_id == user.id, UserProject.project_id == project.id).first()
        if not link:
            db.add(UserProject(user_id=user.id, project_id=project.id, role="lead_architect"))
        if user_id != user.id:
            u_active = db.query(User).filter(User.id == user_id).first()
            if u_active:
                link2 = db.query(UserProject).filter(UserProject.user_id == user_id, UserProject.project_id == project.id).first()
                if not link2:
                    db.add(UserProject(user_id=user_id, project_id=project.id, role="lead_architect"))

    db.commit()
    db.refresh(project)
    return project

@app.get("/api/projects/{project_id}", response_model=ProjectResponse)
def get_project_by_id(project_id: str, db: Session = Depends(get_db)):
    """Retrieve a single project by ID or slug."""
    project = db.query(Project).filter(
        (Project.id == project_id) | (Project.slug == project_id)
    ).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found."
        )
    return project

@app.post("/api/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db)):
    """Register a new project in the database tied to a user ID."""
    project_id = project_in.id or project_in.slug or f"PRJ-{uuid.uuid4().hex[:8].upper()}"
    
    # Check for existing ID or slug
    existing = db.query(Project).filter(
        (Project.id == project_id) | (Project.slug == project_in.slug)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A project with this ID or slug already exists."
        )

    project_data = project_in.model_dump()
    project_data["id"] = project_id
    project = Project(**project_data)
    
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@app.put("/api/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: str, update_in: ProjectUpdate, db: Session = Depends(get_db)):
    """Update an existing project in the database."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found."
        )
    
    update_data = update_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
        
    db.commit()
    db.refresh(project)
    return project

@app.delete("/api/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str, db: Session = Depends(get_db)):
    """Delete a project by ID."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project '{project_id}' not found."
        )
    db.delete(project)
    db.commit()
    return None

# --- Proposals Endpoints (Neon DB) ---

@app.post("/api/proposals", status_code=status.HTTP_201_CREATED)
def submit_proposal(proposal_in: ProposalRequest, db: Session = Depends(get_db)):
    """Submit and persist an academic ADLC research proposal tied to a user ID."""
    proposal_id = f"PROP-{uuid.uuid4().hex[:8].upper()}"
    
    new_proposal = Proposal(
        id=proposal_id,
        **proposal_in.model_dump()
    )
    db.add(new_proposal)
    db.commit()
    db.refresh(new_proposal)

    return {
        "success": True,
        "message": "Proposal submitted successfully! Our lead architects will review your application within 48 business hours.",
        "proposal_id": proposal_id,
        "data": {
            "id": new_proposal.id,
            "user_id": new_proposal.user_id,
            "organization_name": new_proposal.organization_name,
            "contact_email": new_proposal.contact_email,
            "status": new_proposal.status,
            "submitted_at": new_proposal.submitted_at.isoformat() if new_proposal.submitted_at else None
        }
    }

@app.get("/api/users/{user_id}/proposals", response_model=List[ProposalResponse])
def get_user_proposals(user_id: str, db: Session = Depends(get_db)):
    """Retrieve all proposals submitted by a specific signed user ID."""
    return db.query(Proposal).filter(
        Proposal.user_id == user_id
    ).order_by(desc(Proposal.submitted_at)).all()

@app.get("/api/proposals", response_model=List[ProposalResponse])
def list_proposals(db: Session = Depends(get_db)):
    """Retrieve submitted proposals from the database."""
    return db.query(Proposal).order_by(desc(Proposal.submitted_at)).all()

# --- Newsletter Endpoints (Neon DB) ---

@app.post("/api/newsletter", status_code=status.HTTP_200_OK)
def subscribe_newsletter(request: NewsletterRequest, db: Session = Depends(get_db)):
    """Persist newsletter subscriber email into the database."""
    clean_email = request.email.strip().lower()
    if not clean_email or "@" not in clean_email:
        raise HTTPException(status_code=400, detail="Invalid email address.")
    
    existing = db.query(NewsletterSubscriber).filter(NewsletterSubscriber.email == clean_email).first()
    if not existing:
        subscriber = NewsletterSubscriber(email=clean_email)
        db.add(subscriber)
        db.commit()

    return {
        "success": True,
        "message": "Thank you for subscribing to Cognitive Metrics research updates."
    }

# --- Lead Architect Admin & Comment Endpoints ---

@app.get("/api/admin/users", response_model=List[UserResponse])
def get_all_registered_users(db: Session = Depends(get_db)):
    """List registered users for assignment in the Lead Architect console."""
    # Ensure Lead Architect Jeremy Lankford is registered and has lead_architect role
    admin = db.query(User).filter(func.lower(User.email) == "jwlankford@gmail.com").first()
    if not admin:
        admin = User(
            id="Jq4WTmNLN9XbtDqZsbIesLWCTTn1",
            email="jwlankford@gmail.com",
            display_name="Jeremy Lankford",
            role="lead_architect",
            institution="Cognitive Metrics Research Lab",
            department="AI & Systems Architecture"
        )
        db.add(admin)
        db.commit()
    elif admin.role != "lead_architect":
        admin.role = "lead_architect"
        if not admin.display_name:
            admin.display_name = "Jeremy Lankford"
        db.commit()
    return db.query(User).order_by(desc(User.created_at)).all()

@app.get("/api/admin/projects")
def get_admin_projects(db: Session = Depends(get_db)):
    """Retrieve all projects with extra administrative telemetry and comment counts."""
    projects = db.query(Project).order_by(desc(Project.created_at)).all()
    results = []
    for p in projects:
        comment_count = db.query(ProjectComment).filter(ProjectComment.project_id == p.id).count()
        results.append({
            "id": p.id,
            "title": p.title,
            "slug": p.slug,
            "domain": p.domain,
            "status": p.status,
            "status_badge": p.status_badge,
            "phase": p.phase or "Phase 1: Agentic Specification",
            "summary": p.summary,
            "description": p.description,
            "framework": p.framework,
            "lead_architect": p.lead_architect,
            "traces_count": p.traces_count,
            "target_venue": p.target_venue,
            "tags": p.tags or [],
            "repo_url": p.repo_url,
            "demo_url": p.demo_url,
            "production_url": p.production_url,
            "is_active": p.is_active,
            "is_public": p.is_public,
            "user_id": p.user_id,
            "user_email": p.user_email,
            "comment_count": comment_count,
            "created_at": p.created_at.isoformat() if p.created_at else None,
            "updated_at": p.updated_at.isoformat() if p.updated_at else None
        })
    return results

@app.put("/api/admin/projects/{project_id}")
def update_admin_project(
    project_id: str,
    payload: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """Lead Architect update: status, phase, assignment, and project specifications."""
    project = db.query(Project).filter(
        (Project.id == project_id) | (Project.slug == project_id)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")

    update_data = payload.model_dump(exclude_unset=True)

    # Track status/phase changes for audit commentary
    status_changed = "status" in update_data and update_data["status"] != project.status
    phase_changed = "phase" in update_data and update_data["phase"] != project.phase
    old_status = project.status
    old_phase = project.phase

    for key, value in update_data.items():
        setattr(project, key, value)

    if "user_email" in update_data and (not update_data["user_email"] or (isinstance(update_data["user_email"], str) and update_data["user_email"].strip() == "")):
        project.user_email = None

    # If assignment changed, ensure user and user_projects junction table record exist
    if "user_id" in update_data:
        uid = update_data["user_id"]
        if not uid or (isinstance(uid, str) and uid.strip().lower() in ["unassigned", "none", "null", ""]):
            project.user_id = None
            project.user_email = None
            # CRITICAL: Clean up junction table so this project does NOT show up for anyone
            db.query(UserProject).filter(UserProject.project_id == project.id).delete(synchronize_session=False)
        else:
            # Clean up prior junction records for this project so it binds cleanly
            db.query(UserProject).filter(UserProject.project_id == project.id).delete(synchronize_session=False)
            user = db.query(User).filter(User.id == uid).first()
            if not user and project.user_email:
                user = db.query(User).filter(func.lower(User.email) == func.lower(project.user_email)).first()
                if not user:
                    user = User(id=uid, email=project.user_email, display_name=project.user_email.split('@')[0])
                    db.add(user)
                    db.flush()
            if user:
                link = db.query(UserProject).filter(UserProject.user_id == user.id, UserProject.project_id == project.id).first()
                if not link:
                    db.add(UserProject(user_id=user.id, project_id=project.id, role="lead_architect"))
                if uid != user.id:
                    u_active = db.query(User).filter(User.id == uid).first()
                    if u_active:
                        link2 = db.query(UserProject).filter(UserProject.user_id == uid, UserProject.project_id == project.id).first()
                        if not link2:
                            db.add(UserProject(user_id=uid, project_id=project.id, role="lead_architect"))

    # Auto-log audit comment if status or phase changed
    if status_changed or phase_changed:
        log_parts = []
        if status_changed:
            log_parts.append(f"Status changed: '{old_status}' → '{project.status}'")
        if phase_changed:
            log_parts.append(f"Phase changed: '{old_phase}' → '{project.phase}'")
        
        audit_note = ProjectComment(
            project_id=project.id,
            user_id=None,
            author_name="Jeremy Lankford",
            author_role="Lead Architect",
            comment_type="phase_change" if phase_changed else "status_update",
            content="; ".join(log_parts)
        )
        db.add(audit_note)

    db.commit()
    db.refresh(project)

    return {
        "success": True,
        "message": f"Project '{project.title}' updated successfully.",
        "project": {
            "id": project.id,
            "title": project.title,
            "status": project.status,
            "phase": project.phase,
            "user_id": project.user_id,
            "user_email": project.user_email,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
    }

@app.get("/api/projects/{project_id}/comments", response_model=List[ProjectCommentResponse])
def get_project_comments(project_id: str, db: Session = Depends(get_db)):
    """Retrieve all comments, directives, and architect notes for a specific project."""
    return db.query(ProjectComment).filter(
        ProjectComment.project_id == project_id
    ).order_by(desc(ProjectComment.created_at)).all()

@app.post("/api/projects/{project_id}/comments", response_model=ProjectCommentResponse, status_code=status.HTTP_201_CREATED)
def post_project_comment(
    project_id: str,
    comment_in: ProjectCommentCreate,
    db: Session = Depends(get_db)
):
    """Post an architect note, directive, or feedback comment at the project level."""
    project = db.query(Project).filter(
        (Project.id == project_id) | (Project.slug == project_id)
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")

    new_comment = ProjectComment(
        project_id=project.id,
        user_id=comment_in.user_id,
        author_name=comment_in.author_name or "Jeremy Lankford",
        author_email=comment_in.author_email,
        author_role=comment_in.author_role or "Lead Architect",
        comment_type=comment_in.comment_type or "architect_note",
        content=comment_in.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
