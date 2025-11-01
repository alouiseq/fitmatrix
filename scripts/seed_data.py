#!/usr/bin/env python3
"""
Script to seed the database with initial data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models import MuscleGroup, LibraryExercise
from app.core.auth import get_password_hash
from app.models.user import User

def create_muscle_groups(db: Session):
    """Create initial muscle groups"""
    muscle_groups = [
        {
            "name": "chest",
            "display_name": "Chest",
            "description": "Pectoral muscles",
            "color": "#FF6B6B",
            "muscle_names": ["Mid Chest", "Upper Chest", "Lower Chest", "Serratus Anterior"],
            "is_primary": True
        },
        {
            "name": "back",
            "display_name": "Back",
            "description": "Back muscles",
            "color": "#4ECDC4",
            "muscle_names": ["Lats", "Mid Traps", "Upper Traps", "Lower Traps", "Rhomboids", "Erector Spinae", "Teres Major", "Lower Back"],
            "is_primary": True
        },
        {
            "name": "deltoids",
            "display_name": "Deltoids",
            "description": "Deltoid muscles",
            "color": "#45B7D1",
            "muscle_names": ["Front Delts", "Side Delts", "Rear Delts"],
            "is_primary": True
        },
        {
            "name": "biceps",
            "display_name": "Biceps",
            "description": "Bicep muscles",
            "color": "#96CEB4",
            "muscle_names": ["Biceps (Long Head)", "Biceps (Short Head)", "Brachialis"],
            "is_primary": False
        },
        {
            "name": "triceps",
            "display_name": "Triceps",
            "description": "Tricep muscles",
            "color": "#FFEAA7",
            "muscle_names": ["Triceps (Long Head)", "Triceps (Lateral Head)", "Triceps (Medial Head)"],
            "is_primary": False
        },
        {
            "name": "legs",
            "display_name": "Legs",
            "description": "Leg muscles",
            "color": "#DDA0DD",
            "muscle_names": ["Quadriceps", "Hamstrings", "Glutes (Maximus)", "Glutes (Medius)", "Glutes (Minimus)", "Calves", "Hip Flexors", "Tensor Fasciae Latae"],
            "is_primary": True
        },
        {
            "name": "core",
            "display_name": "Core",
            "description": "Abdominal and core muscles",
            "color": "#98D8C8",
            "muscle_names": ["Upper Abs", "Lower Abs", "Obliques", "Serratus Anterior", "Core"],
            "is_primary": True
        },
        {
            "name": "forearms",
            "display_name": "Forearms",
            "description": "Forearm muscles",
            "color": "#F7DC6F",
            "muscle_names": ["Forearm Flexors", "Forearm Extensors", "Forearm Supinators"],
            "is_primary": False
        }
    ]
    
    for group_data in muscle_groups:
        existing = db.query(MuscleGroup).filter(MuscleGroup.name == group_data["name"]).first()
        if not existing:
            muscle_group = MuscleGroup(**group_data)
            db.add(muscle_group)
    
    db.commit()
    print("Muscle groups created successfully!")

def create_library_exercises(db: Session):
    """Create initial library exercises from all_exercises.py"""
    from scripts.all_exercises import allExercises
    from app.models.exercise import LibraryTargetMuscle, ActivationLevel, WeightType
    
    # Get muscle groups mapping
    muscle_groups = {mg.name: mg.id for mg in db.query(MuscleGroup).all()}
    
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
        return "chest"
    
    # Get existing exercise names
    existing_exercises = {ex.name for ex in db.query(LibraryExercise).all()}
    
    # Track exercises we've already processed in this batch
    processed_names = set()
    
    created_count = 0
    for exercise_data in allExercises:
        exercise_name = exercise_data["name"]
        
        # Skip if already exists in database
        if exercise_name in existing_exercises:
            continue
        
        # Skip if already processed in this batch (duplicate in allExercises list)
        if exercise_name in processed_names:
            print(f"Warning: Skipping duplicate exercise '{exercise_name}'")
            continue
        
        processed_names.add(exercise_name)
        
        # Create the library exercise
        library_exercise = LibraryExercise(
            name=exercise_data["name"],
            description=f"Exercise targeting {exercise_data.get('muscleGroup', 'various muscles')}",
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
            equipment=["None"] if exercise_data.get("weightType") == "body" else ["Equipment required"],
            difficulty="Intermediate",  # Default difficulty
            category="Strength",
            is_calisthenics=exercise_data.get("calisthenicsType") is not None,
            calisthenics_type=None,  # We'll handle this later if needed
            muscle_group=exercise_data.get("muscleGroup", "Unknown"),
            weight_type=WeightType(exercise_data.get("weightType", "free")) if exercise_data.get("weightType") else None,
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
    print(f"Library exercises created successfully! ({created_count} new exercises)")

def create_test_user(db: Session):
    """Create a test user"""
    test_user = db.query(User).filter(User.email == "test@example.com").first()
    if not test_user:
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("testpassword")
        )
        db.add(user)
        db.commit()
        print("Test user created successfully!")
    else:
        print("Test user already exists!")

def main():
    """Main function to run all seeding operations"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        create_muscle_groups(db)
        create_library_exercises(db)
        # Skip test user creation - not critical for app functionality
        # Uncomment if you need test user
        # try:
        #     create_test_user(db)
        # except Exception as e:
        #     print(f"Warning: Could not create test user: {e}")
        #     print("Continuing without test user...")
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()