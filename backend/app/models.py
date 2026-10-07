from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String(128), primary_key=True, index=True) # Unique ID (e.g. Firebase UID or UUID)
    email = Column(String(255), unique=True, index=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    role = Column(String(50), default="researcher")
    institution = Column(String(255), nullable=True)
    department = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relational link to projects via junction table
    projects = relationship("UserProject", back_populates="user", cascade="all, delete-orphan")

class UserProject(Base):
    """Junction table establishing many-to-many / table-level relationships between users and projects."""
    __tablename__ = "user_projects"

    user_id = Column(String(128), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    project_id = Column(String(64), ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(50), default="lead_architect") # lead_architect, collaborator, reviewer
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="projects")
    project = relationship("Project", back_populates="assigned_users")

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(128), index=True, nullable=True)     # Direct owner ID
    user_email = Column(String(255), index=True, nullable=True) # Owner email
    title = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    domain = Column(String(255), nullable=False)
    status = Column(String(100), default="Active · ADLC Development")
    status_badge = Column(String(100), default="ADLC Development")
    phase = Column(String(100), default="Phase 1: Agentic Specification")
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    framework = Column(String(255), default="Agentic Development Life Cycle (ADLC)")
    lead_architect = Column(String(255), default="Jeremy Lankford")
    traces_count = Column(Integer, default=0)
    target_venue = Column(String(255), nullable=True)
    tags = Column(JSON, default=list)
    repo_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    production_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relational link to users via junction table
    assigned_users = relationship("UserProject", back_populates="project", cascade="all, delete-orphan")
    # Architect comments and updates stream
    comments = relationship("ProjectComment", back_populates="project", cascade="all, delete-orphan", order_by="desc(ProjectComment.created_at)")

class ProjectComment(Base):
    """Architect audit notes, status update directives, and project-level comments."""
    __tablename__ = "project_comments"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    project_id = Column(String(64), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(128), index=True, nullable=True) # Author user ID who posted the comment
    author_name = Column(String(255), default="Jeremy Lankford")
    author_email = Column(String(255), nullable=True)
    author_role = Column(String(100), default="Lead Architect")
    comment_type = Column(String(50), default="architect_note") # architect_note, status_update, phase_change, directive, project_feedback, question
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="comments")

class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(String(64), primary_key=True, index=True)
    user_id = Column(String(128), index=True, nullable=True)     # Tied to submitting signed user's unique ID
    organization_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=False)
    contact_email = Column(String(255), nullable=False, index=True)
    organization_website = Column(String(500), nullable=True)
    organization_type = Column(String(100), nullable=False)
    selected_services = Column(JSON, nullable=False)
    project_summary = Column(Text, nullable=False)
    target_demographic = Column(Text, nullable=True)
    technical_stack = Column(Text, nullable=True)
    budget_readiness = Column(String(100), nullable=False)
    point_of_contact_confirmed = Column(Boolean, default=False)
    status = Column(String(50), default="pending")
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

class NewsletterSubscriber(Base):
    __tablename__ = "newsletter_subscribers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    subscribed_at = Column(DateTime(timezone=True), server_default=func.now())
