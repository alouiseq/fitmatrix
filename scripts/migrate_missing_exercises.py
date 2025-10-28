#!/usr/bin/env python3
"""
Script to migrate the missing exercises to the database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.exercise import LibraryExercise, LibraryTargetMuscle, ActivationLevel
from app.models.muscle_group import MuscleGroup
from scripts.all_exercises import allExercises

def map_activation_level(level):
    """Map frontend activation level to backend enum"""
    mapping = {
        "maximal": ActivationLevel.MAXIMAL,
        "high": ActivationLevel.HIGH,
        "medium": ActivationLevel.MEDIUM,
        "low": ActivationLevel.LOW
    }
    return mapping.get(level, ActivationLevel.MEDIUM)

def map_muscle_to_group(muscle_name):
    """Map specific muscle names to muscle groups"""
    muscle_name_lower = muscle_name.lower()
    
    # Chest muscles
    if any(chest in muscle_name_lower for chest in ["chest", "pecs", "pectoral"]):
        return "chest"
    
    # Back muscles
    if any(back in muscle_name_lower for back in ["lats", "traps", "rhomboids", "erector spinae", "rear delts"]):
        return "back"
    
    # Shoulder muscles
    if any(shoulder in muscle_name_lower for shoulder in ["delts", "deltoids", "front delts", "side delts"]):
        return "deltoids"
    
    # Arm muscles
    if any(arm in muscle_name_lower for arm in ["biceps", "triceps"]):
        if "biceps" in muscle_name_lower:
            return "biceps"
        elif "triceps" in muscle_name_lower:
            return "triceps"
    
    # Leg muscles
    if any(leg in muscle_name_lower for leg in ["quadriceps", "quads", "hamstrings", "glutes", "calves", "adductors", "abductors"]):
        return "legs"
    
    # Core muscles
    if any(core in muscle_name_lower for core in ["abs", "obliques", "core", "rectus abdominis"]):
        return "core"
    
    # Forearm muscles
    if any(forearm in muscle_name_lower for forearm in ["forearms", "grip"]):
        return "forearms"
    
    # Default fallback
    return "chest"  # Default to chest if unclear

def migrate_missing_exercises():
    """Migrate missing exercises to the database"""
    db = SessionLocal()
    
    try:
        # Get existing exercise names
        existing_exercises = {ex.name for ex in db.query(LibraryExercise).all()}
        print(f"Found {len(existing_exercises)} existing exercises")
        
        # Get muscle groups
        muscle_groups = {mg.name: mg.id for mg in db.query(MuscleGroup).all()}
        print(f"Found muscle groups: {list(muscle_groups.keys())}")
        
        # Find missing exercises
        missing_exercises = []
        for exercise_data in allExercises:
            if exercise_data["name"] not in existing_exercises:
                missing_exercises.append(exercise_data)
        
        print(f"Found {len(missing_exercises)} missing exercises to migrate")
        
        if not missing_exercises:
            print("No missing exercises found!")
            return
        
        # Migrate missing exercises
        created_count = 0
        for exercise_data in missing_exercises:
            print(f"Migrating: {exercise_data['name']}")
            
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
                calisthenics_type=None,  # We'll handle this later if needed
                muscle_group=exercise_data.get("muscleGroup", "Unknown"),
                weight_type=exercise_data.get("weightType", "free"),
                split_types=exercise_data.get("splitTypes", ["perMuscleGroup"])
            )
            
            db.add(library_exercise)
            db.flush()  # Get the ID
            
            # Add target muscles
            for target_muscle in exercise_data.get("targetMuscles", []):
                muscle_name = target_muscle["muscle"]
                muscle_group_name = map_muscle_to_group(muscle_name)
                muscle_group_id = muscle_groups.get(muscle_group_name)
                
                if muscle_group_id is None:
                    print(f"Warning: Muscle group '{muscle_group_name}' not found for {exercise_data['name']}")
                    continue
                
                # Create LibraryTargetMuscle
                library_target_muscle = LibraryTargetMuscle(
                    library_exercise_id=library_exercise.id,
                    muscle_group_id=muscle_group_id,
                    activation_level=map_activation_level(target_muscle["activationLevel"])
                )
                
                db.add(library_target_muscle)
            
            created_count += 1
        
        db.commit()
        print(f"✅ Successfully migrated {created_count} missing exercises")
        
        # Verify the total count
        total_exercises = db.query(LibraryExercise).count()
        total_target_muscles = db.query(LibraryTargetMuscle).count()
        print(f"Total exercises in database: {total_exercises}")
        print(f"Total target muscles in database: {total_target_muscles}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    migrate_missing_exercises()