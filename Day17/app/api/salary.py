from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from app.models.employee import Employee
from app.models.salary import SalaryRecord
from app.schemas.salary import SalaryCalculateRequest, SalaryRecordResponse
from typing import List

router = APIRouter()

@router.post("/calculate", response_model=SalaryRecordResponse)
def calculate_salary(request: SalaryCalculateRequest, db: Session = Depends(get_session)):
    employee = db.exec(select(Employee).where(Employee.id == request.employee_id)).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Core Salary Calculation Logic
    per_day_salary = employee.base_salary / 30
    leave_deduction = per_day_salary * request.unpaid_leaves_taken
    
    # Avoid negative salary if they take too many unpaid leaves
    gross_salary = max(0, employee.base_salary - leave_deduction)
    
    # 5% Flat Tax Deduction
    tax = gross_salary * 0.05
    
    net_salary = gross_salary - tax

    new_salary_record = SalaryRecord(
        employee_id=employee.id,
        month=request.month,
        year=request.year,
        paid_leaves_taken=request.paid_leaves_taken,
        unpaid_leaves_taken=request.unpaid_leaves_taken,
        gross_salary=round(gross_salary, 2),
        tax_deducted=round(tax, 2),
        net_salary=round(net_salary, 2)
    )

    db.add(new_salary_record)
    db.commit()
    db.refresh(new_salary_record)

    return new_salary_record

@router.get("/employee/{employee_id}", response_model=List[SalaryRecordResponse])
def get_employee_salary_records(employee_id: int, db: Session = Depends(get_session)):
    records = db.exec(select(SalaryRecord).where(SalaryRecord.employee_id == employee_id)).all()
    return records
