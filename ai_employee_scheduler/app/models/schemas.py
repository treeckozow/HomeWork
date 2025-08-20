# app/schemas.py
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    role: str  # worker or supervisor
    group: str
    job: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    group: str
    job: str

    model_config = {
        "from_attributes": True,
    }


# Constraint Schemas
class ConstraintCreate(BaseModel):
    user_id: int
    constraint_text: str

class ConstraintResponse(BaseModel):
    id: int
    user_id: int
    constraint_text: str
    structured_data: Optional[Any]
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

# Schedule Schemas
class ScheduleApproval(BaseModel):
    supervisor_id: int
    approved: bool
    comment: Optional[str] = None

class ScheduleResponse(BaseModel):
    id: int
    group: str
    job: str
    schedule_data: dict
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }

