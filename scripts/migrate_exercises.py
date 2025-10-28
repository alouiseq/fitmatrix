#!/usr/bin/env python3
"""
Script to migrate exercises from my-fit-week frontend to fitmatrix backend
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import LibraryExercise, MuscleGroup, TargetMuscle
from app.models.exercise import ActivationLevel, WeightType, CalisthenicsType

# Import the exercise data
from exercise_data import initialExercises

def get_muscle_group_id(db: Session, muscle_name: str) -> int:
    """Find the muscle group ID for a given muscle name"""
    # Map muscle names to muscle group names
    muscle_to_group = {
        # Chest muscles
        "Mid Chest": "chest",
        "Upper Chest": "chest", 
        "Lower Chest": "chest",
        "Serratus Anterior": "core",
        
        # Back muscles
        "Lats": "back",
        "Mid Traps": "back",
        "Upper Traps": "back", 
        "Lower Traps": "back",
        "Rhomboids": "back",
        "Erector Spinae": "back",
        "Teres Major": "back",
        "Lower Back": "back",
        
        # Deltoid muscles
        "Front Delts": "deltoids",
        "Side Delts": "deltoids",
        "Rear Delts": "deltoids",
        
        # Bicep muscles
        "Biceps (Long Head)": "biceps",
        "Biceps (Short Head)": "biceps",
        "Brachialis": "biceps",
        
        # Tricep muscles
        "Triceps (Long Head)": "triceps",
        "Triceps (Lateral Head)": "triceps",
        "Triceps (Medial Head)": "triceps",
        
        # Leg muscles
        "Quadriceps": "legs",
        "Hamstrings": "legs",
        "Glutes (Maximus)": "legs",
        "Glutes (Medius)": "legs",
        "Glutes (Minimus)": "legs",
        "Calves": "legs",
        "Hip Flexors": "legs",
        "Tensor Fasciae Latae": "legs",
        
        # Core muscles
        "Upper Abs": "core",
        "Lower Abs": "core",
        "Obliques": "core",
        "Core": "core",
        
        # Forearm muscles
        "Forearm Flexors": "forearms",
        "Forearm Extensors": "forearms",
        "Forearm Supinators": "forearms",
    }
    
    group_name = muscle_to_group.get(muscle_name, "core")  # Default to core if not found
    muscle_group = db.query(MuscleGroup).filter(MuscleGroup.name == group_name).first()
    if not muscle_group:
        raise ValueError(f"Muscle group not found for muscle: {muscle_name}")
    return muscle_group.id

def map_weight_type(weight_type: str) -> WeightType:
    """Map frontend weight type to backend enum"""
    mapping = {
        "free": WeightType.FREE,
        "body": WeightType.BODY,
        "machine": WeightType.MACHINE
    }
    return mapping.get(weight_type, WeightType.BODY)

def map_activation_level(level: str) -> ActivationLevel:
    """Map frontend activation level to backend enum"""
    mapping = {
        "maximal": ActivationLevel.MAXIMAL,
        "high": ActivationLevel.HIGH,
        "medium": ActivationLevel.MEDIUM,
        "low": ActivationLevel.LOW
    }
    return mapping.get(level, ActivationLevel.MEDIUM)

def map_calisthenics_type(calisthenics_type: str) -> CalisthenicsType:
    """Map frontend calisthenics type to backend enum"""
    mapping = {
        "Planche": CalisthenicsType.PLANCHE,
        "Pull-Ups": CalisthenicsType.PULL_UPS,
        "Muscle-Ups": CalisthenicsType.MUSCLE_UPS,
        "Handstand": CalisthenicsType.HANDSTAND,
        "Push-Ups": CalisthenicsType.PUSH_UPS
    }
    return mapping.get(calisthenics_type)

def migrate_exercises(db: Session):
    """Migrate all exercises from my-fit-week to fitmatrix database"""
    print("Starting exercise migration...")
    
    # Clear existing library exercises
    db.query(TargetMuscle).delete()
    db.query(LibraryExercise).delete()
    db.commit()
    print("Cleared existing exercises")
    
    migrated_count = 0
    
    for exercise_data in initialExercises:
        try:
            # Create the library exercise
            library_exercise = LibraryExercise(
                name=exercise_data["name"],
                description=f"Exercise targeting {exercise_data['muscleGroup']}",
                instructions=[
                    "Start in the proper position",
                    "Execute the movement with control",
                    "Focus on proper form throughout",
                    "Complete the full range of motion"
                ],
                tips=[
                    "Maintain proper breathing",
                    "Keep core engaged",
                    "Focus on the target muscles"
                ],
                equipment=["None"] if exercise_data["weightType"] == "body" else ["Equipment required"],
                difficulty="Intermediate",  # Default difficulty
                category="Strength",
                is_calisthenics=exercise_data.get("calisthenicsType") is not None,
                calisthenics_type=map_calisthenics_type(exercise_data.get("calisthenicsType")),
                muscle_group=exercise_data.get("muscleGroup", "Unknown"),
                weight_type=map_weight_type(exercise_data.get("weightType", "free")),
                split_types=exercise_data.get("splitTypes", ["perMuscleGroup"])
            )
            
            db.add(library_exercise)
            db.flush()  # Get the ID without committing
            
            # Create target muscles
            for target_muscle_data in exercise_data["targetMuscles"]:
                muscle_group_id = get_muscle_group_id(db, target_muscle_data["muscle"])
                activation_level = map_activation_level(target_muscle_data["activationLevel"])
                
                target_muscle = TargetMuscle(
                    exercise_id=library_exercise.id,
                    muscle_group_id=muscle_group_id,
                    activation_level=activation_level
                )
                db.add(target_muscle)
            
            migrated_count += 1
            if migrated_count % 10 == 0:
                print(f"Migrated {migrated_count} exercises...")
                
        except Exception as e:
            print(f"Error migrating exercise {exercise_data.get('name', 'Unknown')}: {e}")
            continue
    
    db.commit()
    print(f"Successfully migrated {migrated_count} exercises!")

def main():
    """Main function to run the migration"""
    db = SessionLocal()
    
    try:
        migrate_exercises(db)
        print("Exercise migration completed successfully!")
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()