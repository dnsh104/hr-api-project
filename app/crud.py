from sqlalchemy.orm import Session
from . import models, schemas


# ── Request CRUD ───────────────────────────────────────────────────────────────

def create_request(db: Session, request: schemas.RequestCreate):
    db_request = models.Request(
        employee_name=request.employee_name,
        check_type=request.check_type
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_requests(db: Session):
    return db.query(models.Request).all()


def get_request(db: Session, request_id: int):
    return db.query(models.Request).filter(models.Request.id == request_id).first()


def update_request_status(db: Session, request_id: int, status: schemas.StatusType):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if request:
        request.status = status
        db.commit()
        db.refresh(request)
    return request


def delete_request(db: Session, request_id: int):
    request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if request:
        db.delete(request)
        db.commit()
    return request


# ── Report CRUD ────────────────────────────────────────────────────────────────

def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(
        request_id=report.request_id,
        agency=report.agency,
        result=report.result
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_reports(db: Session):
    return db.query(models.Report).all()


def get_report(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()


def get_reports_by_request(db: Session, request_id: int):
    return db.query(models.Report).filter(models.Report.request_id == request_id).all()


def delete_report(db: Session, report_id: int):
    report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if report:
        db.delete(report)
        db.commit()
    return report