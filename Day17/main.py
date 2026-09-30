from fastapi import FastAPI
from database import create_tables

# Import models to ensure they are registered with SQLModel
from app.models.employee import Employee
from app.models.salary import SalaryRecord

# Import API Routers
from app.api import employees, salary

app = FastAPI(title="Salary Management System Backend")

@app.on_event("startup")
def on_startup():
    create_tables()

# Register Routes
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])
app.include_router(salary.router, prefix="/api/salary", tags=["Salary"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Salary Management API"}
