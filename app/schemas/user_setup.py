from pydantic import BaseModel
from typing import List
from app.models.user_setup import SetupSplitType, WorkoutDay, WorkoutFocusType, RecommendType, WorkoutLength

class UserSetupConfigBase(BaseModel):
    split_type: SetupSplitType
    workout_days: List[WorkoutDay]
    workout_focus: WorkoutFocusType
    recommend_type: RecommendType
    workout_length: WorkoutLength
    selected_muscle_groups: List[int] = []
    is_completed: bool = False

class UserSetupConfigCreate(UserSetupConfigBase):
    pass

class UserSetupConfigResponse(UserSetupConfigBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class UserSetupConfig(UserSetupConfigBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True