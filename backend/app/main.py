from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
import datetime

app = FastAPI(title="Cognitive Metrics API", version="1.0.0")

# Enable CORS for local dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProposalRequest(BaseModel):
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

class NewsletterRequest(BaseModel):
    email: str

# In-memory storage for demonstration / local dev
PROPOSALS_DB = []
NEWSLETTER_DB = []

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Cognitive Metrics API",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.post("/api/proposals")
def submit_proposal(proposal: ProposalRequest):
    proposal_id = f"PROP-{uuid.uuid4().hex[:8].upper()}"
    record = {
        "id": proposal_id,
        "submitted_at": datetime.datetime.utcnow().isoformat(),
        **proposal.model_dump()
    }
    PROPOSALS_DB.append(record)
    return {
        "success": True,
        "message": "Proposal submitted successfully! Our product leads will review your application within 48 business hours.",
        "proposal_id": proposal_id,
        "data": record
    }

@app.post("/api/newsletter")
def subscribe_newsletter(request: NewsletterRequest):
    if not request.email or "@" not in request.email:
        raise HTTPException(status_code=400, detail="Invalid email address.")
    NEWSLETTER_DB.append({
        "email": request.email,
        "subscribed_at": datetime.datetime.utcnow().isoformat()
    })
    return {
        "success": True,
        "message": "Thank you for subscribing to Cognitive Metrics updates."
    }
