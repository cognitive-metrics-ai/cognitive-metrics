import logging
from sqlalchemy.orm import Session
from .models import Project

logger = logging.getLogger("cognitive_metrics.seed")

INITIAL_PROJECTS = [
    {
        "id": "fluid-guardian",
        "title": "fluid-guardian application",
        "slug": "fluid-guardian",
        "domain": "Clinical Fluid Monitoring & Telemetry",
        "status": "Active · ADLC Development",
        "status_badge": "ADLC Development",
        "summary": "Safety-critical clinical fluid monitoring and volume telemetry application developed using autonomous agent workflows with human-in-the-loop verification under the ADLC protocol.",
        "description": "The fluid-guardian application serves as an experimental testbed for hospital patient fluid intake/output monitoring, designed from ground up using the Agentic Development Life Cycle (ADLC). It logs developer cognitive load, agent task delegation traces, and multi-tier verification safety rubrics.",
        "framework": "Agentic Development Life Cycle (ADLC)",
        "lead_architect": "Jeremy Lankford",
        "user_id": "Jq4WTmNLN9XbtDqZsbIesLWCTTn1",
        "user_email": "jwlankford@gmail.com",
        "traces_count": 22400,
        "target_venue": "Clinical Fluid Monitoring · ADLC Research",
        "tags": ["Clinical Telemetry", "Agentic Synthesis", "Safety Verification", "Trace Logging"],
        "repo_url": "https://github.com/cognitive-metrics-ai/fluid-guardian",
        "demo_url": None,
        "production_url": "https://fluid-guardian.cognitivemetrics.app/",
        "is_active": True
    },
    {
        "id": "employee-performance-management",
        "title": "Employee Performance Management System",
        "slug": "employee-performance-management",
        "domain": "Enterprise Evaluation & Workflow Suite",
        "status": "Active · ADLC Development",
        "status_badge": "ADLC Development",
        "summary": "Full-lifecycle workforce evaluation, goal tracking, and review platform engineered utilizing multi-agent ADLC orchestration and empirical cognitive friction profiling.",
        "description": "Constructed to evaluate multi-agent architectural coordination on enterprise CRUD and analytical workflows. It measures latency overhead, agent verification gates, and cognitive fatigue during high-velocity software cycles under ADLC methodologies.",
        "framework": "Agentic Development Life Cycle (ADLC)",
        "lead_architect": "Jeremy Lankford",
        "user_id": "Jq4WTmNLN9XbtDqZsbIesLWCTTn1",
        "user_email": "jwlankford@gmail.com",
        "traces_count": 16850,
        "target_venue": "Enterprise Systems · ADLC Architecture",
        "tags": ["Enterprise Architecture", "Multi-Agent Orchestration", "Cognitive Profiling", "ADLC Telemetry"],
        "repo_url": "https://github.com/cognitive-metrics-ai/epms",
        "demo_url": None,
        "production_url": None,
        "is_active": True
    },
    {
        "id": "PROP-ADLC-9042",
        "title": "Human-in-the-Loop ADLC Code Synthesis Testbed",
        "slug": "human-in-the-loop-code-synthesis",
        "domain": "Software Engineering & HCI Testbed",
        "status": "Approved · Implementation Active",
        "status_badge": "Implementation Active",
        "summary": "Full-stack experimental IDE testbed measuring developer cognitive load, latency, and autonomous agent handoff dynamics.",
        "description": "Designed and engineered an experimental IDE testbed measuring developer cognitive load, interruption recovery latency, and task completion fidelity during autonomous agent code synthesis.",
        "framework": "Agentic Development Life Cycle (ADLC)",
        "lead_architect": "Jeremy Lankford",
        "traces_count": 14290,
        "target_venue": "Target: ICSE / CHI 2027",
        "tags": ["ADLC Metrics", "Cognitive Load", "FastAPI", "Vue 3", "Eye-Tracking Hook"],
        "repo_url": None,
        "demo_url": None,
        "production_url": None,
        "is_active": True
    },
    {
        "id": "PROP-ADLC-8411",
        "title": "Clinical Diagnostic Agent Verification Protocol",
        "slug": "clinical-diagnostic-agent-verification",
        "domain": "Biomedical Informatics Research",
        "status": "Protocol Scoped · Pending Pilot",
        "status_badge": "Pending Pilot",
        "summary": "Multi-agent orchestration testbed evaluating physician trust calibration and double-blind verification safety rubrics.",
        "description": "Multi-agent orchestration testbed allowing medical researchers to evaluate physician trust calibration, cognitive friction, and autonomous verification protocols in healthcare workflows.",
        "framework": "Agentic Development Life Cycle (ADLC)",
        "lead_architect": "Jeremy Lankford",
        "traces_count": 3100,
        "target_venue": "Target: JAMIA / AMIA 2027",
        "tags": ["Clinical ADLC", "Multi-Agent Systems", "Safety Auditing", "Python"],
        "repo_url": None,
        "demo_url": None,
        "production_url": None,
        "is_active": True
    }
]

def seed_initial_projects(db: Session):
    """Seed initial project records if the table is empty, and ensure default URLs and owner assignments are populated."""
    from .models import UserProject
    existing_count = db.query(Project).count()
    if existing_count == 0:
        logger.info("Projects table is empty. Seeding initial ADLC projects into database...")
        for p_data in INITIAL_PROJECTS:
            project = Project(**p_data)
            db.add(project)
            if p_data.get("user_id"):
                db.add(UserProject(user_id=p_data["user_id"], project_id=p_data["id"], role="lead_architect"))
        db.commit()
        logger.info("Successfully seeded %d projects.", len(INITIAL_PROJECTS))
    else:
        logger.info("Database already contains %d projects. Checking for missing metadata and assignments...", existing_count)
        for p in db.query(Project).all():
            if p.id == "fluid-guardian" and not p.production_url:
                p.production_url = "https://fluid-guardian.cognitivemetrics.app/"
            if p.lead_architect and "jeremy" in p.lead_architect.lower():
                if not p.user_id:
                    p.user_id = "Jq4WTmNLN9XbtDqZsbIesLWCTTn1"
                if not p.user_email:
                    p.user_email = "jwlankford@gmail.com"
                link = db.query(UserProject).filter(
                    UserProject.user_id == p.user_id,
                    UserProject.project_id == p.id
                ).first()
                if not link:
                    db.add(UserProject(user_id=p.user_id, project_id=p.id, role="lead_architect"))
        db.commit()
        logger.info("Project metadata and default owner assignments verified.")

def seed_initial_users(db: Session):
    """Seed or update Lead Architect Jeremy Lankford in the users table."""
    from .models import User
    admin = db.query(User).filter(User.email == "jwlankford@gmail.com").first()
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
        logger.info("Seeded Lead Architect Jeremy Lankford into users table.")
    elif admin.role != "lead_architect":
        admin.role = "lead_architect"
        if not admin.display_name:
            admin.display_name = "Jeremy Lankford"
        db.commit()
        logger.info("Updated Jeremy Lankford role to lead_architect in users table.")
