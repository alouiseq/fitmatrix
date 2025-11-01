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
    """Create initial library exercises"""
    exercises = [
        {
            "name": "Push-ups",
            "description": "Classic bodyweight exercise for chest, shoulders, and triceps",
            "instructions": [
                "Start in a plank position with hands slightly wider than shoulders",
                "Lower your body until chest nearly touches the floor",
                "Push back up to starting position",
                "Keep core tight throughout the movement"
            ],
            "tips": [
                "Keep your body in a straight line",
                "Don't let your hips sag or pike up",
                "Breathe out on the way up"
            ],
            "equipment": ["None"],
            "difficulty": "Beginner",
            "category": "Strength",
            "is_calisthenics": True,
            "calisthenics_type": "Push-Ups"
        },
        {
            "name": "Pull-ups",
            "description": "Upper body pulling exercise targeting back and biceps",
            "instructions": [
                "Hang from a pull-up bar with palms facing away",
                "Pull your body up until chin clears the bar",
                "Lower yourself with control to starting position",
                "Keep core engaged throughout"
            ],
            "tips": [
                "Start with assisted pull-ups if needed",
                "Focus on pulling with your back, not just arms",
                "Full range of motion is important"
            ],
            "equipment": ["Pull-up Bar"],
            "difficulty": "Intermediate",
            "category": "Strength",
            "is_calisthenics": True,
            "calisthenics_type": "Pull-Ups"
        },
        {
            "name": "Squats",
            "description": "Fundamental lower body exercise",
            "instructions": [
                "Stand with feet shoulder-width apart",
                "Lower your body as if sitting back into a chair",
                "Go down until thighs are parallel to floor",
                "Push through heels to return to standing"
            ],
            "tips": [
                "Keep knees tracking over toes",
                "Chest up, core tight",
                "Weight in heels"
            ],
            "equipment": ["None"],
            "difficulty": "Beginner",
            "category": "Strength",
            "is_calisthenics": False
        }
    ]
    
    for exercise_data in exercises:
        existing = db.query(LibraryExercise).filter(LibraryExercise.name == exercise_data["name"]).first()
        if not existing:
            exercise = LibraryExercise(**exercise_data)
            db.add(exercise)
    
    db.commit()
    print("Library exercises created successfully!")

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