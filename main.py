from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task API",
    version="1.0"
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
    return tasks


# =========================
# GET /tasks/{id}
# =========================

@app.get(
    "/tasks/{id}",
    description="Get a task by ID"
)
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
# POST /tasks
# =========================

@app.post(
    "/tasks",
    status_code=201,
    description="Create a new task"
)
def create_task(task: TaskCreate):

    # Check empty title
    if not task.title.strip():

        return JSONResponse(
            status_code=400,
            content={
                "error": "title must not be empty"
            }
        )

    # Generate next ID
    new_id = max(
        [task["id"] for task in tasks],
        default=0
    ) + 1

    # Create task
    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

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
def update_task(
    id: int,
    task_update: TaskUpdate
):

    # Find task
    for task in tasks:

        if task["id"] == id:

            # Check that at least one field was provided
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

            # Update title if provided
            if task_update.title is not None:

                if not task_update.title.strip():

                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "title must not be empty"
                        }
                    )

                task["title"] = task_update.title

            # Update done if provided
            if task_update.done is not None:

                task["done"] = task_update.done

            return task

    # Task not found
    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )


# =========================
# DELETE /tasks/{id}
# =========================

@app.delete(
    "/tasks/{id}",
    status_code=204,
    description="Delete a task"
)
def delete_task(id: int):

    for task in tasks:

        if task["id"] == id:

            tasks.remove(task)

            return

    return JSONResponse(
        status_code=404,
        content={
            "error": f"Task {id} not found"
        }
    )