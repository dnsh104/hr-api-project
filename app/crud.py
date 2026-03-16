from sqlalchemy.orm import Session
from . import models, schemas


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


def update_request_status(db: Session, request_id: int, status: str):
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