from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
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

@router.get("/stats/progress")
def get_workout_progress_stats(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workout progress statistics for the Progress page"""
    from sqlalchemy import func
    from app.models.exercise import Exercise, TargetMuscle
    from app.models.muscle_group import MuscleGroup
    
    # Get completed workouts from the last N days
    start_date = datetime.utcnow() - timedelta(days=days)
    workouts = db.query(Workout).filter(
        Workout.user_id == current_user.id,
        Workout.completed_at.isnot(None),
        Workout.completed_at >= start_date
    ).all()
    
    # For now, return mock data since we don't have real workout data
    # In a real app, you would calculate this from actual workout data
    mock_workouts = []
    for i in range(min(15, days)):
        workout_date = datetime.utcnow() - timedelta(days=i)
        mock_workouts.append({
            "date": workout_date.isoformat(),
            "exercises": 4 + (i % 3),
            "sets": 10 + (i % 5),
            "volume": 8000 + (i * 200),
            "muscleGroups": {
                "Chest": {"reps": 30 + (i % 10), "volume": 2000 + (i * 100)},
                "Back": {"reps": 35 + (i % 8), "volume": 2500 + (i * 120)},
                "Legs": {"reps": 40 + (i % 12), "volume": 3000 + (i * 150)},
            }
        })
    
    return mock_workouts