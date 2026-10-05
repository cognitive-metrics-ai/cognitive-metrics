from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Project Schemas ---
class ProjectBase(BaseModel):
    user_id: Optional[str] = Field(None, example="user_2p8X... or google-demo-user-123")
    user_email: Optional[str] = Field(None, example="researcher@university.edu")
    title: str = Field(..., example="fluid-guardian application")
    slug: str = Field(..., example="fluid-guardian")
    domain: str = Field(..., example="Clinical Fluid Monitoring & Telemetry")
    status: str = Field(default="Active · ADLC Development")
    status_badge: str = Field(default="ADLC Development")
    phase: str = Field(default="Phase 1: Agentic Specification")
    summary: str = Field(..., example="Safety-critical clinical fluid monitoring application...")
    description: Optional[str] = None
    framework: str = Field(default="Agentic Development Life Cycle (ADLC)")
    lead_architect: str = Field(default="Jeremy Lankford")
    traces_count: int = Field(default=0)
    target_venue: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_active: bool = True
    is_public: bool = True

class ProjectCreate(ProjectBase):
    id: Optional[str] = None

class ProjectUpdate(BaseModel):
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    title: Optional[str] = None
    slug: Optional[str] = None
    domain: Optional[str] = None
    status: Optional[str] = None
    status_badge: Optional[str] = None
    phase: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    framework: Optional[str] = None
    lead_architect: Optional[str] = None
    traces_count: Optional[int] = None
    target_venue: Optional[str] = None
    tags: Optional[List[str]] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None

class ProjectResponse(ProjectBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Project Comment Schemas ---
class ProjectCommentCreate(BaseModel):
    user_id: Optional[str] = None
    author_name: str = "Jeremy Lankford"
    author_email: Optional[str] = None
    author_role: str = "Lead Architect"
    comment_type: str = "architect_note" # architect_note, status_update, phase_change, directive, feedback
    content: str

class ProjectCommentResponse(BaseModel):
    id: int
    project_id: str
    user_id: Optional[str] = None
    author_name: str
    author_email: Optional[str] = None
    author_role: str
    comment_type: str
    content: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Proposal Schemas ---
class ProposalRequest(BaseModel):
    user_id: Optional[str] = None
    organization_name: str
    contact_name: str
    contact_email: str
    organization_website: Optional[str] = None
    organization_type: str
    selected_services: List[str]
    project_summary: str
    target_demographic: Optional[str] = None
    technical_stack: Optional[str] = None
    budget_readiness: str
    point_of_contact_confirmed: bool

class ProposalResponse(ProposalRequest):
    id: str
    status: str
    submitted_at: datetime

    class Config:
        from_attributes = True

# --- Newsletter Schemas ---
class NewsletterRequest(BaseModel):
    email: str

class NewsletterResponse(BaseModel):
    email: str
    subscribed_at: datetime

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserSyncRequest(BaseModel):
    id: str = Field(..., description="Firebase UID or unique user ID")
    email: str
    display_name: Optional[str] = None
    institution: Optional[str] = None
    department: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    display_name: Optional[str] = None
    role: str
    institution: Optional[str] = None
    department: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
