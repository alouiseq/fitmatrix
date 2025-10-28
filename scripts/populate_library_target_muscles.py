#!/usr/bin/env python3
"""
Script to populate library_target_muscles table with target muscle data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models.exercise import LibraryExercise, LibraryTargetMuscle
from app.models.muscle_group import MuscleGroup
from app.models.exercise import ActivationLevel
from scripts.exercise_data import initialExercises

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

def populate_library_target_muscles():
    """Populate library_target_muscles table"""
    db = SessionLocal()
    
    try:
        # Get all library exercises
        library_exercises = db.query(LibraryExercise).all()
        print(f"Found {len(library_exercises)} library exercises")
        
        # Get muscle groups
        muscle_groups = {mg.name: mg.id for mg in db.query(MuscleGroup).all()}
        print(f"Found muscle groups: {list(muscle_groups.keys())}")
        
        # Create a mapping from exercise name to target muscles from original data
        exercise_target_muscles = {}
        for exercise_data in initialExercises:
            exercise_name = exercise_data["name"]
            target_muscles = exercise_data.get("targetMuscles", [])
            exercise_target_muscles[exercise_name] = target_muscles
        
        print(f"Found target muscle data for {len(exercise_target_muscles)} exercises")
        
        # Populate library_target_muscles
        created_count = 0
        for library_exercise in library_exercises:
            exercise_name = library_exercise.name
            target_muscles = exercise_target_muscles.get(exercise_name, [])
            
            print(f"Processing {exercise_name}: {len(target_muscles)} target muscles")
            
            for target_muscle in target_muscles:
                muscle_name = target_muscle["muscle"]
                # Map specific muscle names to muscle groups
                muscle_group_name = map_muscle_to_group(muscle_name)
                muscle_group_id = muscle_groups.get(muscle_group_name)
                
                if muscle_group_id is None:
                    print(f"Warning: Muscle group '{muscle_group_name}' not found for {exercise_name}")
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
        print(f"✅ Created {created_count} library target muscle records")
        
        # Verify the data
        total_library_target_muscles = db.query(LibraryTargetMuscle).count()
        print(f"Total library target muscles in database: {total_library_target_muscles}")
        
        # Show some examples
        sample_exercises = db.query(LibraryExercise).limit(3).all()
        for exercise in sample_exercises:
            target_muscles = db.query(LibraryTargetMuscle).filter(
                LibraryTargetMuscle.library_exercise_id == exercise.id
            ).all()
            print(f"{exercise.name}: {len(target_muscles)} target muscles")
            for tm in target_muscles:
                muscle_group = db.query(MuscleGroup).filter(MuscleGroup.id == tm.muscle_group_id).first()
                print(f"  - {muscle_group.name} ({tm.activation_level})")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_library_target_muscles()