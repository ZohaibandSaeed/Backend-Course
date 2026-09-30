from pydantic import BaseModel

class EmployeeBase(BaseModel):
    name: str
    department: str
    base_salary: float
    allowed_paid_leaves: int = 15

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
