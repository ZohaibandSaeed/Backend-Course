from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_session
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_session)):
    db_employee = Employee.model_validate(employee)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@router.get("/", response_model=List[EmployeeResponse])
def get_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    employees = db.exec(select(Employee).offset(skip).limit(limit)).all()
    return employees
