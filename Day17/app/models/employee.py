from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    department: str
    base_salary: float
    allowed_paid_leaves: int = Field(default=5)

    salary_records: List["SalaryRecord"] = Relationship(back_populates="employee")
