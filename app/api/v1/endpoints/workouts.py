from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.models.workout import Workout, WorkoutExercise
from app.models.user import User
from app.schemas.workout import WorkoutResponse, WorkoutCreate, WorkoutExerciseCreate
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[WorkoutResponse])
def get_user_workouts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workouts = db.query(Workout).filter(Workout.user_id == current_user.id).all()
    return workouts

@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.post("/", response_model=WorkoutResponse)
def create_workout(
    workout: WorkoutCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create the workout
    workout_data = workout.dict()
    exercises = workout_data.pop("exercises", [])
    
    db_workout = Workout(
        **workout_data,
        user_id=current_user.id
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    
    # Add exercises to workout
    for exercise in exercises:
        exercise["workout_id"] = db_workout.id
        db_exercise = WorkoutExercise(**exercise)
        db.add(db_exercise)
    
    db.commit()
    return db_workout

@router.put("/{workout_id}/complete")
def complete_workout(
    workout_id: int,
    duration_minutes: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    workout.completed_at = datetime.utcnow()
    workout.duration_minutes = duration_minutes
    db.commit()
    
    return {"message": "Workout completed successfully"}

@router.delete("/{workout_id}")
def delete_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    db.delete(workout)
    db.commit()
    
    return {"message": "Workout deleted successfully"}