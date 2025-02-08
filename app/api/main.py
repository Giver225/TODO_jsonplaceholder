from fastapi import FastAPI
from app.api.routes.tasks import router as tasks_router

app = FastAPI()

app.include_router(tasks_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}