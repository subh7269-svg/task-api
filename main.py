from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel

app = FastAPI()


# =========================
# Request Models
# =========================

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


# =========================
# Validation Error Handler
# =========================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"error": "title is required"}
    )


# =========================
# In-Memory Task Data
# =========================

tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build CRUD API",
        "done": False
    },
    {
        "id": 3,
        "title": "Push project to GitHub",
        "done": True
    }
]


# =========================
# Stage 1
# Root Endpoint
# =========================

@app.get("/", description="Get information about the Task API")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# =========================
# Stage 1
# Health Endpoint
# =========================

@app.get("/health", description="Check whether the API is running")
def health():
    return {
        "status": "ok"
    }


# =========================
# Stage 2
# Get All Tasks
# =========================

@app.get("/tasks", description="Get all tasks")
def get_tasks():
    return tasks


# =========================
# Stage 2
# Get Single Task
# =========================

@app.get("/tasks/{id}", description="Get a task by ID")
def get_task(id: int):

    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )


# =========================
# Stage 3
# Create Task
# =========================

@app.post(
    "/tasks",
    status_code=201,
    description="Create a new task"
)
def create_task(task: TaskCreate):

    # Check for empty title
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={
                "error": "title must not be empty"
            }
        )

    # Generate next ID
    new_id = max(
        [t["id"] for t in tasks],
        default=0
    ) + 1

    # Create new task
    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    # Add task to list
    tasks.append(new_task)

    return new_task


# =========================
# Stage 4
# Update Task
# =========================

@app.put(
    "/tasks/{id}",
    description="Update a task"
)
def update_task(
    id: int,
    task_update: TaskUpdate
):

    for task in tasks:

        if task["id"] == id:

            task["title"] = task_update.title
            task["done"] = task_update.done

            return task

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )


# =========================
# Stage 4
# Delete Task
# =========================

@app.delete(
    "/tasks/{id}",
    description="Delete a task"
)
def delete_task(id: int):

    for task in tasks:

        if task["id"] == id:

            tasks.remove(task)

            return {
                "message": f"Task {id} deleted"
            }

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )