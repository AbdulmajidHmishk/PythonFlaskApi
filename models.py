from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Base model for an employee
class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of the employee")
    email: EmailStr = Field(..., description="Employee's email address")
    position: Optional[str] = Field(None, max_length=100, description="Job position")
    start_date: Optional[datetime] = Field(None, description="Start date of employment")

# Model for creating a new employee (includes salary)
class EmployeeCreate(EmployeeBase):
    salary: Optional[float] = Field(None, ge=0, description="Salary (optional)")

# Model for updating an employee (all fields optional)
class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    position: Optional[str] = Field(None, max_length=100)
    salary: Optional[float] = Field(None, ge=0)

# Model for responses (without salary for privacy)
class Employee(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
