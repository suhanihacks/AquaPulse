from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

SourceType = Literal["real", "derived", "simulated"]
VerificationStatus = Literal["pending", "confirmed", "rejected", "insufficient_evidence"]

class CitizenReport(BaseModel):
    segment_id: str
    category: str
    severity: float = Field(0.5, ge=0, le=1)
    description: str = ""

class VerificationAction(BaseModel):
    status: VerificationStatus
    note: str = ""
    segment_id: str | None = None
    event_id: str | None = None
