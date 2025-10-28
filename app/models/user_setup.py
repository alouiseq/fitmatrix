from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class SetupSplitType(str, enum.Enum):
    UPPER_LOWER = "upperLower"
    PUSH_PULL_LEGS = "pushPullLegs"
    PER_MUSCLE_GROUP = "perMuscleGroup"
    CALISTHENICS = "calisthenics"

class WorkoutDay(str, enum.Enum):
    MON = "mon"
    TUE = "tue"
    WED = "wed"
    THU = "thu"
    FRI = "fri"
    SAT = "sat"
    SUN = "sun"

class WorkoutFocusType(str, enum.Enum):
    RESISTANCE_TRAINING = "resistanceTraining"
    CALISTHENICS = "calisthenics"
    MIXED = "mixed"

class RecommendType(str, enum.Enum):
    FULLY_AUTO = "fullyAuto"
    PARTIAL_AUTO = "partialAuto"
    MANUAL = "manual"

class WorkoutLength(str, enum.Enum):
    THIRTY = "30"
    SIXTY = "60"
    NINETY = "90"
    ONE_TWENTY = "120"

class UserSetupConfig(Base):
    __tablename__ = "user_setup_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    split_type = Column(Enum(SetupSplitType), nullable=False)
    workout_days = Column(JSON, nullable=False)
    workout_focus = Column(Enum(WorkoutFocusType), nullable=False)
    recommend_type = Column(Enum(RecommendType), nullable=False)
    workout_length = Column(Enum(WorkoutLength), nullable=False)
    selected_muscle_groups = Column(JSON)  # IDs of selected muscle groups
    is_completed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="setup_config")