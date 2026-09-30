from pydantic import BaseModel

class SalaryCalculateRequest(BaseModel):
    employee_id: int
    month: str
    year: int
    paid_leaves_taken: int
    unpaid_leaves_taken: int

class SalaryRecordResponse(BaseModel):
    id: int
    employee_id: int
    month: str
    year: int
    paid_leaves_taken: int
    unpaid_leaves_taken: int
    gross_salary: float
    tax_deducted: float
    net_salary: float

    class Config:
        from_attributes = True
