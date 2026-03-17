from pydantic import BaseModel
from enum import Enum
from typing import List, Optional


class CheckType(str, Enum):
    dbs = "DBS"
    credit = "Credit"
    bank = "Bank"
    home_office = "Home Office"


class StatusType(str, Enum):
    pending = "Pending"
    in_progress = "In Progress"
    completed = "Completed"
    rejected = "Rejected"


# ── Request schemas ────────────────────────────────────────────────────────────

class RequestCreate(BaseModel):
    employee_name: str
    check_type: CheckType


class RequestStatusUpdate(BaseModel):
    status: StatusType


class Request(BaseModel):
    id: int
    employee_name: str
    check_type: str
    status: str
    reports: List["Report"] = []

    class Config:
        from_attributes = True


# ── Report schemas ─────────────────────────────────────────────────────────────

class ReportCreate(BaseModel):
    request_id: int
    agency: str
    result: str


class Report(BaseModel):
    id: int
    request_id: int
    agency: str
    result: str

    class Config:
        from_attributes = True


Request.model_rebuild()