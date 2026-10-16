from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.database import engine
from app.models.health_worker import HealthWorker
from app.routes.health_workers import router as health_worker_router
from app.routes.auth import router as auth_router
from app.models.pregnant_woman import PregnantWoman
from app.routes.pregnant_women import router as pregnant_woman_router
from app.routes import screening
from app.routes import ml_prediction
app = FastAPI(
    title="MotherCareAI API",
    description="Maternal Health Decision Support System",
    version="0.1.0",
)


# Allow the React frontend to communicate with the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API routes
app.include_router(health_worker_router)
app.include_router(auth_router)
app.include_router(pregnant_woman_router)
app.include_router(screening.router)
app.include_router(ml_prediction.router)

@app.get("/")
def root():
    return {
        "message": "MotherCareAI API is running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MotherCareAI API",
    }


@app.get("/database-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "result": result.scalar(),
        }