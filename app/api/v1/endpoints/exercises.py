from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.exercise import Exercise, LibraryExercise, TargetMuscle, LibraryTargetMuscle
from app.schemas.exercise import ExerciseResponse, LibraryExerciseResponse, ExerciseCreate, LibraryExerciseCreate

router = APIRouter()

@router.get("/library", response_model=List[LibraryExerciseResponse])
def get_library_exercises(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    is_calisthenics: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    from sqlalchemy.orm import joinedload
    
    query = db.query(LibraryExercise).options(joinedload(LibraryExercise.target_muscles))
    
    if category:
        query = query.filter(LibraryExercise.category == category)
    if difficulty:
        query = query.filter(LibraryExercise.difficulty == difficulty)
    if is_calisthenics is not None:
        query = query.filter(LibraryExercise.is_calisthenics == is_calisthenics)
    
    exercises = query.offset(skip).limit(limit).all()
    return exercises

@router.get("/library/{exercise_id}", response_model=LibraryExerciseResponse)
def get_library_exercise(exercise_id: int, db: Session = Depends(get_db)):
    from sqlalchemy.orm import joinedload
    
    exercise = db.query(LibraryExercise).options(joinedload(LibraryExercise.target_muscles)).filter(LibraryExercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/library", response_model=LibraryExerciseResponse)
def create_library_exercise(exercise: LibraryExerciseCreate, db: Session = Depends(get_db)):
    db_exercise = LibraryExercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.get("/", response_model=List[ExerciseResponse])
def get_exercises(
    skip: int = 0,
    limit: int = 100,
    weight_type: Optional[str] = None,
    muscle_group_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Exercise)
    
    if weight_type:
        query = query.filter(Exercise.weight_type == weight_type)
    
    exercises = query.offset(skip).limit(limit).all()
    return exercises

@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.post("/", response_model=ExerciseResponse)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    # Create the exercise
    exercise_data = exercise.dict()
    target_muscles = exercise_data.pop("target_muscles", [])
    
    db_exercise = Exercise(**exercise_data)
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    
    # Add target muscles
    for target_muscle in target_muscles:
        target_muscle["exercise_id"] = db_exercise.id
        db_target_muscle = TargetMuscle(**target_muscle)
        db.add(db_target_muscle)
    
    db.commit()
    return db_exercise