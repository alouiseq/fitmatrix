from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.workout import SplitType

class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    order: int
    sets: Optional[int] = None
    reps: Optional[str] = None
    weight: Optional[str] = None
    rest_seconds: Optional[int] = None
    notes: Optional[str] = None

class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass

class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: int
    exercise: Optional[dict] = None
    
    class Config:
        from_attributes = True

class WorkoutExercise(WorkoutExerciseBase):
    id: int
    exercise: Optional[dict] = None
    
    class Config:
        from_attributes = True

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    split_type: SplitType
    scheduled_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    notes: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate] = []

class WorkoutResponse(WorkoutBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    exercises: List[WorkoutExerciseResponse] = []
    
    class Config:
        from_attributes = True

class Workout(WorkoutBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    exercises: List[WorkoutExercise] = []
    
    class Config:
        from_attributes = True