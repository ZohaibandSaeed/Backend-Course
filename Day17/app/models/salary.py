from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .employee import Employee

class SalaryRecord(SQLModel, table=True):
    __tablename__ = "salary_records"
    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="employees.id")
    month: str
    year: int
    present_days: int = Field(default=0)
    paid_leaves_taken: int = Field(default=0)
    unpaid_leaves_taken: int = Field(default=0)
    gross_salary: float
    tax_deducted: float
    net_salary: float

    employee: Optional[Employee] = Relationship(back_populates="salary_records")
