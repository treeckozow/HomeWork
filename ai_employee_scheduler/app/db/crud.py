# app/crud.py
from sqlalchemy.orm import Session
from app.models import schemas #app.
from app.models import models #app.

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        email=user.email,
        role=user.role,
        group=user.group,
        job=user.job
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users_by_group_and_role(db: Session, group: str, role: str, job: str):
    return db.query(models.User).filter(models.User.group == group, models.User.role == role, models.User.job == job).all()

def get_supervisor_by_group(db: Session, group: str, job: str):
    return db.query(models.User).filter(models.User.group == group, models.User.role == "supervisor", models.User.job == job).first()

# Constraint CRUD
def create_constraint(db: Session, constraint: schemas.ConstraintCreate, structured_data: dict):
    db_constraint = models.Constraint(
        user_id=constraint.user_id,
        constraint_text=constraint.constraint_text,
        structured_data=structured_data
    )
    db.add(db_constraint)
    db.commit()
    db.refresh(db_constraint)
    return db_constraint

def get_constraints_by_group_and_job(db: Session, group: str, job: str):
    # Retrieves constraints for users in the specified group and job
    from sqlalchemy.orm import joinedload
    constraints = db.query(models.Constraint)\
        .join(models.User, models.User.id == models.Constraint.user_id)\
        .filter(models.User.group == group, models.User.job == job)\
        .all()
    return constraints

# Schedule CRUD
def create_schedule(db: Session, group: str, job: str, schedule_data: dict):
    db_schedule = models.Schedule(
        group=group,
        job=job,
        schedule_data=schedule_data,
        status="pending"
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_schedule(db: Session, schedule_id: int):
    return db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()

def update_schedule(db: Session, schedule: models.Schedule):
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule
