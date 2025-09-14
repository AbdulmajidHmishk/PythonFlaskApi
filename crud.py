from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import EmployeeDB
from models import EmployeeCreate, EmployeeUpdate
from datetime import datetime

# CREATE employee
def create_employee(db: Session, employee: EmployeeCreate):
    # Check for duplicate email
    existing = db.query(EmployeeDB).filter(EmployeeDB.email == employee.email).first()
    if existing:
        raise ValueError("Email already exists")
    
    db_employee = EmployeeDB(
        name=employee.name,
        email=employee.email,
        position=employee.position,
        start_date=employee.start_date,
        salary=employee.salary,
        created_at=datetime.utcnow()
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# READ all employees
def get_all_employees(db: Session):
    employees = db.query(EmployeeDB).all()
    return employees

# READ one employee by ID
def get_employee(db: Session, employee_id: int):
    employee = db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()
    if not employee:
        raise ValueError("Employee not found")
    return employee

# UPDATE employee
def update_employee(db: Session, employee_id: int, update_data: EmployeeUpdate):
    employee = db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()
    if not employee:
        raise ValueError("Employee not found")
    
    # Check for email duplicate if changed
    if update_data.email and update_data.email != employee.email:
        existing = db.query(EmployeeDB).filter(EmployeeDB.email == update_data.email).first()
        if existing:
            raise ValueError("Email already exists")
    
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(employee, field, value)
    employee.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(employee)
    return employee

# DELETE employee
def delete_employee(db: Session, employee_id: int):
    employee = db.query(EmployeeDB).filter(EmployeeDB.id == employee_id).first()
    if not employee:
        raise ValueError("Employee not found")
    
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}
