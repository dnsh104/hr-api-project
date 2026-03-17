from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    check_type = Column(String, nullable=False)
    status = Column(String, default="Pending")

    reports = relationship("Report", back_populates="request")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)
    agency = Column(String, nullable=False)
    result = Column(String, nullable=False)

    request = relationship("Request", back_populates="reports")