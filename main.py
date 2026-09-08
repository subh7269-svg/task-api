from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from pydantic import BaseModel

app = FastAPI()


class TaskCreate(BaseModel):
    title: str


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"error": "title is required"}
    )


@app.get("/", description="Get information about the Task API")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health", description="Check whether the API is running")
def health():
    return {
        "status": "ok"
    }


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


@app.get("/tasks", description="Get all tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{id}", description="Get a task by ID")
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task

    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )


@app.post("/tasks", status_code=201, description="Create a new task")
def create_task(task: TaskCreate):
    if not task.title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title must not be empty"}
        )

    new_id = max([t["id"] for t in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }

    tasks.append(new_task)

    return new_task