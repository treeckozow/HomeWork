from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from controller import router
from StudentManager import StudentManager

@asynccontextmanager
async def lifeSpan(app: FastAPI):
    app.state.StudentManager = StudentManager()
    yield 

app = FastAPI(
    lifespan=lifeSpan,
    title="students database",
    description="gui for sql students database"
    )
app.include_router(router=router) 
 
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)


