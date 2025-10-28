from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.muscle_group import MuscleGroup
from app.schemas.muscle_group import MuscleGroupResponse, MuscleGroupCreate

router = APIRouter()

@router.get("/", response_model=List[MuscleGroupResponse])
def get_muscle_groups(
    skip: int = 0,
    limit: int = 100,
    is_primary: bool = None,
    db: Session = Depends(get_db)
):
    query = db.query(MuscleGroup)
    
    if is_primary is not None:
        query = query.filter(MuscleGroup.is_primary == is_primary)
    
    muscle_groups = query.offset(skip).limit(limit).all()
    return muscle_groups

@router.get("/{muscle_group_id}", response_model=MuscleGroupResponse)
def get_muscle_group(muscle_group_id: int, db: Session = Depends(get_db)):
    muscle_group = db.query(MuscleGroup).filter(MuscleGroup.id == muscle_group_id).first()
    if not muscle_group:
        raise HTTPException(status_code=404, detail="Muscle group not found")
    return muscle_group

@router.post("/", response_model=MuscleGroupResponse)
def create_muscle_group(muscle_group: MuscleGroupCreate, db: Session = Depends(get_db)):
    db_muscle_group = MuscleGroup(**muscle_group.dict())
    db.add(db_muscle_group)
    db.commit()
    db.refresh(db_muscle_group)
    return db_muscle_group