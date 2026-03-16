from pydantic import BaseModel


class RequestCreate(BaseModel):
    employee_name: str
    check_type: str


class Request(BaseModel):
    id: int
    employee_name: str
    check_type: str
    status: str

    class Config:
        from_attributes = True


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