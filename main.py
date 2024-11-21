from fastapi import FastAPI, HTTPException, APIRouter, Depends, Request
from typing import Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get the API Key from environment variables
API_KEY = os.getenv("LAB4_KEY")

# Check if API key is provided
def verify_api_key(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key

# Define task database
task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

# Task model for input validation
class Task(BaseModel):
    task_title: str
    task_desc: Optional[str] = ""
    is_finished: bool = False

# APIV1 Router (Version 1)
apiv1 = APIRouter()

@apiv1.get("/task/{task_id}", tags=["Version 1"])
def get_task_v1(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    return task

@apiv1.post("/task", tags=["Version 1"])
def create_task_v1(task: Task, api_key: str = Depends(verify_api_key)):
    task_id = len(task_db) + 1
    new_task = task.dict()
    new_task["task_id"] = task_id
    task_db.append(new_task)
    return JSONResponse(status_code=201, content={"message": "Task successfully created.", "task": new_task})

@apiv1.patch("/task/{task_id}", tags=["Version 1"])
def update_task_v1(task_id: int, task: Task, api_key: str = Depends(verify_api_key)):
    task_db_entry = next((task for task in task_db if task["task_id"] == task_id), None)
    if not task_db_entry:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    task_db_entry.update(task.dict())
    return JSONResponse(status_code=204, content={"message": "Task successfully updated."})

@apiv1.delete("/task/{task_id}", tags=["Version 1"])
def delete_task_v1(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    task_db.remove(task)
    return JSONResponse(status_code=204, content={"message": "Task successfully deleted."})

# APIV2 Router (Version 2)
apiv2 = APIRouter()

@apiv2.get("/task/{task_id}", tags=["Version 2"])
def get_task_v2(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    return task

@apiv2.post("/task", tags=["Version 2"])
def create_task_v2(task: Task, api_key: str = Depends(verify_api_key)):
    task_id = len(task_db) + 1
    new_task = task.dict()
    new_task["task_id"] = task_id
    task_db.append(new_task)
    return JSONResponse(status_code=201, content={"message": "Task successfully created.", "task": new_task})

@apiv2.patch("/task/{task_id}", tags=["Version 2"])
def update_task_v2(task_id: int, task: Task, api_key: str = Depends(verify_api_key)):
    task_db_entry = next((task for task in task_db if task["task_id"] == task_id), None)
    if not task_db_entry:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    task_db_entry.update(task.dict())
    return JSONResponse(status_code=204, content={"message": "Task successfully updated."})

@apiv2.delete("/task/{task_id}", tags=["Version 2"])
def delete_task_v2(task_id: int, api_key: str = Depends(verify_api_key)):
    task = next((task for task in task_db if task["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found.")
    task_db.remove(task)
    return JSONResponse(status_code=204, content={"message": "Task successfully deleted."})

# Include the routers in the main app
app.include_router(apiv1, prefix="/apiv1", tags=["Version 1"])
app.include_router(apiv2, prefix="/apiv2", tags=["Version 2"])