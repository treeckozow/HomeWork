import json
import app.models.schemas as schemas #app.
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks
from app.db.database import SessionLocal

router = APIRouter()

#Getting all stored globals
async def get_crud(request: Request):
    return request.app.state.crud
async def get_models(request: Request):
    return request.app.state.models
async def get_notifications(request: Request):
    return request.app.state.notifications
async def get_scheduler(request: Request):
    return request.app.state.scheduler

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/register",
    response_model=schemas.UserResponse
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    crud=Depends(get_crud)
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db, user)
    return new_user

@router.post(
    "/submit_constraint",
    response_model=schemas.ConstraintResponse
)
def submit_constraint(
    constraint: schemas.ConstraintCreate,
    db: Session = Depends(get_db),
    crud=Depends(get_crud),
    scheduler=Depends(get_scheduler)
):
    user = crud.get_user(db, constraint.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Process free text using ChatGPT API (ai_processing module)
    structured = scheduler.process_employee_constraint(constraint.constraint_text)
    new_constraint = crud.create_constraint(db, constraint, structured)
    return new_constraint

@router.get("/schedule/generate")
def generate_schedule_endpoint(
    group: str,
    job: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    crud=Depends(get_crud),
    scheduler=Depends(get_scheduler),
    notifications=Depends(get_notifications)
):
    # Ensure all workers in the group have submitted constraints
    workers = crud.get_users_by_group_and_role(db, group=group, role="worker", job=job)
    constraints = crud.get_constraints_by_group_and_job(db, group=group, job=job)
    if len(constraints) < len(workers):
        raise HTTPException(status_code=400, detail="Not all workers have submitted constraints")
    # Generate the schedule
    schedule_data = scheduler.generate_schedule(db, group=group, job=job)
    schedule = crud.create_schedule(db, group=group, job=job, schedule_data=schedule_data)
    # Notify supervisor that schedule is ready for review
    supervisor = crud.get_supervisor_by_group(db, group=group, job=job)
    if supervisor:
        background_tasks.add_task(
            notifications.send_notification,
            supervisor.email,
            f"Schedule for {group} - {job} is ready for approval."
        )
    return {"message": "Schedule generated and awaiting supervisor approval, ID=" + str(schedule.id) + ", schedule:" + json.dumps(schedule_data)}

@router.post("/schedule/approval")
def approve_schedule(
    schedule_id: int,
    approval: schemas.ScheduleApproval,
    db: Session = Depends(get_db),
    crud=Depends(get_crud),
    notifications=Depends(get_notifications)
):
    schedule = crud.get_schedule(db, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    # Check supervisor authorization
    supervisor = crud.get_user(db, approval.supervisor_id)
    if not supervisor or supervisor.role != "supervisor" or supervisor.group != schedule.group:
        raise HTTPException(status_code=403, detail="Not authorized")
    schedule.status = "routerroved" if approval.routerroved else "rejected"
    crud.update_schedule(db, schedule)
    # Notify workers if schedule is routerroved
    if approval.routerroved:
        workers = crud.get_users_by_group_and_role(db, group=schedule.group, role="worker", job=schedule.job)
        for worker in workers:
            notifications.send_notification(worker.email, f"New schedule for {schedule.group} - {schedule.job} is published.")
    return {"message": "Schedule approval updated", "schedule_status": schedule.status}
