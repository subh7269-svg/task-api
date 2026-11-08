from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
from database import (
    init_db,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Task API",
    version="1.0",
    lifespan=lifespan
)

# =========================
# Request Models
# =========================

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


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
        content={
            "error": "Invalid request body"
        }
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
# GET /
# =========================

@app.get(
    "/",
    description="Get information about the Task API"
)
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


# =========================
# GET /health
# =========================

@app.get(
    "/health",
    description="Check whether the API is running"
)
def health():
    return {
        "status": "ok"
    }


# =========================
# GET /tasks
# =========================
@app.get(
    "/tasks",
    description="Get all tasks"
)
def get_tasks():

    return get_all_tasks()


# =========================
# GET /tasks/{id}
# =========================

@app.get(
    "/tasks/{id}",
    description="Get a task by ID"
)
def get_task(id: int):

    task = get_task_by_id(id)

    if task is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": "Task not found"
            }
        )

    return task


# =========================
# POST /tasks
# =========================

@app.post(
    "/tasks",
    status_code=201,
    description="Create a new task"
)
def create_new_task(task: TaskCreate):

    # Validate empty title
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={
                "error": "title must not be empty"
            }
        )

    # Save task in SQLite
    new_task = create_task(task.title)

    return new_task

    # Add task
    tasks.append(new_task)

    return new_task


# =========================
# PUT /tasks/{id}
# =========================


@app.put(
    "/tasks/{id}",
    description="Update a task"
)
def update_existing_task(
    id: int,
    task_update: TaskUpdate
):

    # Validate that at least one field is provided
    if (
        task_update.title is None
        and task_update.done is None
    ):
        return JSONResponse(
            status_code=400,
            content={
                "error": "Provide title or done"
            }
        )

    # Validate empty title
    if (
        task_update.title is not None
        and not task_update.title.strip()
    ):
        return JSONResponse(
            status_code=400,
            content={
                "error": "title must not be empty"
            }
        )

    updated = update_task(
        id,
        task_update.title,
        task_update.done
    )

    if updated is None:
        return JSONResponse(
            status_code=404,
            content={
                "error": f"Task {id} not found"
            }
        )

    return updated



# =========================
# DELETE /tasks/{id}
# =========================


@app.delete(
    "/tasks/{id}",
    status_code=204,
    description="Delete a task"
)
def delete_existing_task(id: int):

    deleted = delete_task(id)

    if not deleted:
        return JSONResponse(
            status_code=404,
            content={
                "error": f"Task {id} not found"
            }
        )

    return None
