from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все домены (для разработки)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Подключение маршрутов
from app.api.routes.tasks import router as tasks_router
from app.api.routes.auth import router as auth_router

app.include_router(tasks_router)
app.include_router(auth_router)



@app.get("/")
def read_root():
    return {"message": "Hello, World!"}