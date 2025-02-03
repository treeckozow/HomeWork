from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

tasks = {}
id = 0

async def isTaskValid(my_task):
    if not my_task or "title" not in my_task or "description" not in my_task:
        return False
    return True

async def taskInvalidError():
    return HTTPException(status_code= 400, detail= "Bad Request, data must include 'title' and 'description'")

async def notFoundError():
    return HTTPException(status_code= 404, detail= "Task not found")

@app.get("/tasks") # get all tasks
async def getTasks():
    return tasks

@app.post("/tasks") # post new task
async def createTask(task: dict[str, str]):
    global id
    if not await isTaskValid(task):
        return await taskInvalidError()
    id += 1
    task["completed"] = False
    task["id"] = id
    tasks[id] = task
    return task

@app.get("/tasks/{task_id}") # get task bt id
async def getTaskById(task_id: int):
    if task_id in tasks:
        return tasks[task_id]
    return await notFoundError()

@app.put("/tasks/{task_id}") # change exicting task
async def modifyTask(task_id: int, task: dict[str, str]):
    if task_id in tasks:
        if not await isTaskValid(task):
            return await taskInvalidError()
        task["id"] = task_id
        task["completed"] = tasks[task_id]["completed"]
        tasks[task_id] = task
        return task
    return await notFoundError()

@app.delete("/tasks/{task_id}") # delete task by id
async def deleteTask(task_id: int):
    if task_id in tasks:
        del tasks[task_id]
        return HTTPException(status_code= 200, detail= "Task deleted successfully")
    return await notFoundError()

@app.get("/tasks/{task_id}/completed") # mark task as completed
async def markAsCompleted(task_id: int):
    if task_id in tasks:
        tasks[task_id]["completed"] = True
        return HTTPException(status_code= 200, detail= "Task marked as completed")
    return await notFoundError()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)