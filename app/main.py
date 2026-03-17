from fastapi import FastAPI, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from .database import SessionLocal, engine, Base
from . import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Regent College London — HR Background Check System")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# ── DB Dependency ──────────────────────────────────────────────────────────────

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── UI Route ───────────────────────────────────────────────────────────────────

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    requests = crud.get_requests(db)
    pending = len([r for r in requests if r.status == "Pending"])
    in_progress = len([r for r in requests if r.status == "In Progress"])
    completed = len([r for r in requests if r.status == "Completed"])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "requests": requests,
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
    })


# ── Request Routes ─────────────────────────────────────────────────────────────

@app.post("/add")
def add_request(
    employee_name: str = Form(...),
    check_type: str = Form(...),
    db: Session = Depends(get_db)
):
    new_request = schemas.RequestCreate(
        employee_name=employee_name,
        check_type=check_type
    )
    crud.create_request(db, new_request)
    return RedirectResponse(url="/", status_code=303)


@app.get("/requests", response_model=List[schemas.Request])
def list_requests(db: Session = Depends(get_db)):
    return crud.get_requests(db)


@app.get("/requests/{request_id}", response_model=schemas.Request)
def get_request(request_id: int, db: Session = Depends(get_db)):
    request = crud.get_request(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request


@app.put("/requests/{request_id}/status", response_model=schemas.Request)
def update_status(
    request_id: int,
    body: schemas.RequestStatusUpdate,
    db: Session = Depends(get_db)
):
    updated = crud.update_request_status(db, request_id, body.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Request not found")
    return updated


@app.delete("/requests/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_request(db, request_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": f"Request {request_id} deleted successfully"}


# ── Report Routes ──────────────────────────────────────────────────────────────

@app.post("/reports", response_model=schemas.Report)
def create_report(report: schemas.ReportCreate, db: Session = Depends(get_db)):
    # Ensure the linked request exists
    linked = crud.get_request(db, report.request_id)
    if not linked:
        raise HTTPException(status_code=404, detail="Linked request not found")
    return crud.create_report(db, report)


@app.get("/reports", response_model=List[schemas.Report])
def list_reports(db: Session = Depends(get_db)):
    return crud.get_reports(db)


@app.get("/reports/{report_id}", response_model=schemas.Report)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = crud.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@app.get("/requests/{request_id}/reports", response_model=List[schemas.Report])
def get_reports_for_request(request_id: int, db: Session = Depends(get_db)):
    linked = crud.get_request(db, request_id)
    if not linked:
        raise HTTPException(status_code=404, detail="Request not found")
    return crud.get_reports_by_request(db, request_id)


@app.delete("/reports/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_report(db, report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"message": f"Report {report_id} deleted successfully"}