from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine, Base
from . import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HR Background Check API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "HR Reporting System API"}
    

@app.post("/requests", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db, request)


@app.get("/requests", response_model=list[schemas.Request])
def read_requests(db: Session = Depends(get_db)):
    return crud.get_requests(db)


@app.get("/requests/{request_id}", response_model=schemas.Request)
def read_request(request_id: int, db: Session = Depends(get_db)):

    request = crud.get_request(db, request_id)

    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return request


@app.put("/requests/{request_id}")
def update_request(request_id: int, status: str, db: Session = Depends(get_db)):

    request = crud.update_request_status(db, request_id, status)

    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return request


@app.delete("/requests/{request_id}")
def delete_request(request_id: int, db: Session = Depends(get_db)):

    request = crud.delete_request(db, request_id)

    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return {"message": "Request deleted"}