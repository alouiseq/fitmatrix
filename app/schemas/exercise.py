from pydantic import BaseModel
from typing import List, Optional
from app.models.exercise import WeightType, ActivationLevel, CalisthenicsType

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
    muscle_group: Optional[str] = None
    weight_type: Optional[WeightType] = None
    split_types: List[str] = []

class LibraryExerciseCreate(LibraryExerciseBase):
    pass

class LibraryTargetMuscleResponse(BaseModel):
    id: int
    muscle_group_id: int
    activation_level: ActivationLevel
    
    class Config:
        from_attributes = True

class LibraryExerciseResponse(LibraryExerciseBase):
    id: int
    target_muscles: List[LibraryTargetMuscleResponse] = []
    
    class Config:
        from_attributes = True

class LibraryExercise(LibraryExerciseBase):
    id: int
    
    class Config:
        from_attributes = True