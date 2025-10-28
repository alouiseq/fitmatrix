#!/usr/bin/env python3
"""
Script to extract ALL exercises from the my-fit-week TypeScript file
"""

import re
import json
import os

def extract_exercises_from_ts():
    """Extract all exercises from the TypeScript file"""
    ts_file_path = "/Users/alouiseq/code/my-fit-week/src/data/exercises.ts"
    
    if not os.path.exists(ts_file_path):
        print(f"TypeScript file not found: {ts_file_path}")
        return []
    
    with open(ts_file_path, 'r') as f:
        content = f.read()
    
    # Find the initialExercises array
    start_marker = "export const initialExercises = ["
    end_marker = "];"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print("Could not find initialExercises array")
        return []
    
    start_idx += len(start_marker)
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        print("Could not find end of initialExercises array")
        return []
    
    exercises_text = content[start_idx:end_idx]
    
    # Parse exercises using regex
    exercises = []
    
    # Pattern to match each exercise object
    exercise_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    
    # Find all exercise objects
    matches = re.finditer(exercise_pattern, exercises_text, re.DOTALL)
    
    for match in matches:
        exercise_text = match.group(0)
        
        # Extract basic fields
        name_match = re.search(r'name:\s*["\']([^"\']+)["\']', exercise_text)
        id_match = re.search(r'id:\s*["\']([^"\']+)["\']', exercise_text)
        muscle_group_match = re.search(r'muscleGroup:\s*["\']([^"\']+)["\']', exercise_text)
        weight_type_match = re.search(r'weightType:\s*["\']([^"\']+)["\']', exercise_text)
        
        if name_match and id_match:
            exercise = {
                "id": id_match.group(1),
                "name": name_match.group(1),
                "muscleGroup": muscle_group_match.group(1) if muscle_group_match else "Unknown",
                "weightType": weight_type_match.group(1) if weight_type_match else "free",
                "targetMuscles": [],
                "splitTypes": []
            }
            
            # Extract target muscles
            target_muscles_match = re.search(r'targetMuscles:\s*\[(.*?)\]', exercise_text, re.DOTALL)
            if target_muscles_match:
                target_muscles_text = target_muscles_match.group(1)
                muscle_matches = re.finditer(r'\{[^}]*muscle[^}]*activationLevel[^}]*\}', target_muscles_text)
                for muscle_match in muscle_matches:
                    muscle_text = muscle_match.group(0)
                    muscle_name_match = re.search(r'muscle:\s*["\']([^"\']+)["\']', muscle_text)
                    activation_match = re.search(r'activationLevel:\s*["\']([^"\']+)["\']', muscle_text)
                    
                    if muscle_name_match and activation_match:
                        exercise["targetMuscles"].append({
                            "muscle": muscle_name_match.group(1),
                            "activationLevel": activation_match.group(1)
                        })
            
            # Extract split types
            split_types_match = re.search(r'splitTypes:\s*\[(.*?)\]', exercise_text)
            if split_types_match:
                split_types_text = split_types_match.group(1)
                split_matches = re.findall(r'["\']([^"\']+)["\']', split_types_text)
                exercise["splitTypes"] = split_matches
            
            exercises.append(exercise)
    
    return exercises

if __name__ == "__main__":
    exercises = extract_exercises_from_ts()
    print(f"Extracted {len(exercises)} exercises")
    
    # Save to file
    with open("/Users/alouiseq/code/fitmatrix/scripts/all_exercises.py", "w") as f:
        f.write("# All exercises extracted from my-fit-week\n")
        f.write("allExercises = ")
        f.write(json.dumps(exercises, indent=2))
    
    print("Saved to scripts/all_exercises.py")
    
    # Show first few exercises
    print("\nFirst 5 exercises:")
    for i, exercise in enumerate(exercises[:5]):
        print(f"{i+1}. {exercise['name']} ({exercise['muscleGroup']}) - {len(exercise['targetMuscles'])} target muscles")