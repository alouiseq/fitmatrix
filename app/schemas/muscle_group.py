from pydantic import BaseModel
from typing import List, Optional

class MuscleGroupBase(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None
    color: Optional[str] = None
    muscle_names: List[str] = []
    is_primary: bool = False

class MuscleGroupCreate(MuscleGroupBase):
    pass

class MuscleGroupResponse(MuscleGroupBase):
    id: int
    
    class Config:
        from_attributes = True

class MuscleGroup(MuscleGroupBase):
    id: int
    
    class Config:
        from_attributes = True