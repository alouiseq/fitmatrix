from sqlalchemy import Column, Integer, String, Text, Boolean, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class WeightType(str, enum.Enum):
    FREE = "free"
    BODY = "body"
    MACHINE = "machine"

class ActivationLevel(str, enum.Enum):
    MAXIMAL = "maximal"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class CalisthenicsType(str, enum.Enum):
    PLANCHE = "Planche"
    PULL_UPS = "Pull-Ups"
    MUSCLE_UPS = "Muscle-Ups"
    HANDSTAND = "Handstand"
    PUSH_UPS = "Push-Ups"

class TargetMuscle(Base):
    __tablename__ = "target_muscles"
    
    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    muscle_group_id = Column(Integer, ForeignKey("muscle_groups.id"))
    activation_level = Column(Enum(ActivationLevel), nullable=False)
    
    # Relationships
    exercise = relationship("Exercise", back_populates="target_muscles")
    muscle_group = relationship("MuscleGroup")

class LibraryExercise(Base):
    __tablename__ = "library_exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    instructions = Column(JSON)  # Step-by-step instructions
    tips = Column(JSON)  # Exercise tips
    equipment = Column(JSON)  # Required equipment
    difficulty = Column(String)  # Beginner, Intermediate, Advanced
    category = Column(String)  # Strength, Cardio, Flexibility, etc.
    is_calisthenics = Column(Boolean, default=False)
    calisthenics_type = Column(Enum(CalisthenicsType), nullable=True)
    
    # Relationships
    exercises = relationship("Exercise", back_populates="library_exercise")

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    library_exercise_id = Column(Integer, ForeignKey("library_exercises.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    weight_type = Column(Enum(WeightType), nullable=False)
    type = Column(String, nullable=False)  # 'free', 'body', 'machine'
    
    # Relationships
    library_exercise = relationship("LibraryExercise", back_populates="exercises")
    target_muscles = relationship("TargetMuscle", back_populates="exercise")
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise")