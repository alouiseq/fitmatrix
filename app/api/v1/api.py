from fastapi import APIRouter
from app.api.v1.endpoints import users, exercises, workouts, muscle_groups, user_setup

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(exercises.router, prefix="/exercises", tags=["exercises"])
api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(muscle_groups.router, prefix="/muscle-groups", tags=["muscle-groups"])
api_router.include_router(user_setup.router, prefix="/user-setup", tags=["user-setup"])