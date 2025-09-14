from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Employee, EmployeeCreate, EmployeeUpdate
import crud

app = FastAPI(title="Employee Management API")

# Health Check
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "employee-api"}

# CREATE employee
@app.post("/employees", response_model=Employee, status_code=status.HTTP_201_CREATED)
def create_employee_endpoint(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_employee(db, employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ all employees
@app.get("/employees", response_model=List[Employee])
def get_all_employees_endpoint(db: Session = Depends(get_db)):
    return crud.get_all_employees(db)

# READ one employee by ID
@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_employee(db, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# UPDATE employee
@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee_endpoint(employee_id: int, update_data: EmployeeUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_employee(db, employee_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# DELETE employee
@app.delete("/employees/{employee_id}")
def delete_employee_endpoint(employee_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_employee(db, employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
