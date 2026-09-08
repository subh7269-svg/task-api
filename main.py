from fastapi import FastAPI

app = FastAPI()


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