from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class SplitType(str, enum.Enum):
    PULL = "pull"
    PUSH = "push"
    UPPER = "upper"
    LOWER = "lower"
    LEGS = "legs"
    ABS = "abs"
    PER_MUSCLE_GROUP = "perMuscleGroup"
    CALISTHENICS = "calisthenics"

class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    split_type = Column(Enum(SplitType), nullable=False)
    scheduled_date = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="workouts")
    exercises = relationship("WorkoutExercise", back_populates="workout")

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("library_exercises.id"))
    order = Column(Integer, nullable=False)  # Order within the workout
    sets = Column(Integer)
    reps = Column(String)  # Can be "8-12" or "AMRAP" etc.
    weight = Column(String)  # Can be "bodyweight" or specific weight
    rest_seconds = Column(Integer)
    notes = Column(Text)
    
    # Relationships
    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("LibraryExercise", back_populates="workout_exercises")