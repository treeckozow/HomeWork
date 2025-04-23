# app/main.py
# import os
from contextlib import asynccontextmanager 
from fastapi import FastAPI 
import app.models.models as models #app.
import app.schedule.notifications as notifications #app.
from app.db import crud #app.
from app.schedule import scheduler #app.
from app.db.database import engine 
from fastapi.middleware.cors import CORSMiddleware 
from app.controller import router #app.
import uvicorn


#Create and store globals
@asynccontextmanager
async def lifeSpan(app: FastAPI):
    app.state.crud          = crud
    app.state.models        = models
    app.state.notifications = notifications
    app.state.scheduler     = scheduler
    # Create database tables
    models.Base.metadata.create_all(bind=engine)    
    yield

#wire up FastAPI with lifespan handler
app = FastAPI(
    lifespan=lifeSpan,
    title="AI Scheduler App",
    description="AI-Powered Employee Scheduling System"
    )
app.include_router(router=router)

# Allow CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

