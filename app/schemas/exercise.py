from pydantic import BaseModel
from typing import List, Optional
from app.models.exercise import WeightType, ActivationLevel, CalisthenicsType

class TargetMuscleBase(BaseModel):
    muscle_group_id: int
    activation_level: ActivationLevel

class TargetMuscleCreate(TargetMuscleBase):
    pass

class TargetMuscleResponse(TargetMuscleBase):
    id: int
    muscle_group: Optional[dict] = None
    
    class Config:
        from_attributes = True

class LibraryExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    instructions: List[str] = []
    tips: List[str] = []
    equipment: List[str] = []
    difficulty: Optional[str] = None
    category: Optional[str] = None
    is_calisthenics: bool = False
    calisthenics_type: Optional[CalisthenicsType] = None

class LibraryExerciseCreate(LibraryExerciseBase):
    pass

class LibraryExerciseResponse(LibraryExerciseBase):
    id: int
    
    class Config:
        from_attributes = True

class LibraryExercise(LibraryExerciseBase):
    id: int
    
    class Config:
        from_attributes = True

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    weight_type: WeightType
    type: str

class ExerciseCreate(ExerciseBase):
    library_exercise_id: int
    target_muscles: List[TargetMuscleCreate] = []

class ExerciseResponse(ExerciseBase):
    id: int
    library_exercise: Optional[LibraryExercise] = None
    target_muscles: List[TargetMuscleResponse] = []
    
    class Config:
        from_attributes = True

class Exercise(ExerciseBase):
    id: int
    library_exercise: Optional[LibraryExercise] = None
    target_muscles: List[TargetMuscleResponse] = []
    
    class Config:
        from_attributes = True