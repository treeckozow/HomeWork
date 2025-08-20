# app/scheduler.py
from app.db import crud #app.
from app.schedule import ai_processing #app.

from sqlalchemy.orm import Session

from app.models import models #app.

def process_employee_constraint(constraint_text: str) -> dict:
    """
    Convert free-text constraint into structured data using the ChatGPT API.
    """
    structured = ai_processing.process_constraint(constraint_text)
    return structured

def generate_schedule(db: Session, group: str, job: str) -> dict:
    """
    A simple round-robin scheduling algorithm:
      - Retrieves all constraints for a given group and job.
      - Assigns shifts fairly to each worker.
      - Returns a schedule as a dict mapping user_id to assigned shift and constraints.
    """
    workers = crud.get_users_by_group_and_role(db, group=group, role="worker", job=job)
    constraints = crud.get_constraints_by_group_and_job(db, group=group, job=job)
    
    # For demonstration, assign shifts in a round-robin manner.
    schedule = {}
    shifts = ["Morning", "Afternoon", "Night"]
    for idx, worker in enumerate(workers):
        schedule[worker.id] = {
            "worker_name": worker.name,
            "assigned_shift": shifts[idx % len(shifts)],
            "constraints": [c.structured_data for c in constraints if c.user_id == worker.id]
        }
    return schedule
