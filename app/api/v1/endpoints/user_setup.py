from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.user_setup import UserSetupConfig
from app.schemas.user_setup import UserSetupConfigResponse, UserSetupConfigCreate
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=UserSetupConfigResponse)
def get_user_setup(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    setup = db.query(UserSetupConfig).filter(UserSetupConfig.user_id == current_user.id).first()
    if not setup:
        raise HTTPException(status_code=404, detail="User setup not found")
    return setup

@router.post("/", response_model=UserSetupConfigResponse)
def create_user_setup(
    setup: UserSetupConfigCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if setup already exists
    existing_setup = db.query(UserSetupConfig).filter(UserSetupConfig.user_id == current_user.id).first()
    if existing_setup:
        raise HTTPException(status_code=400, detail="User setup already exists")
    
    db_setup = UserSetupConfig(
        **setup.dict(),
        user_id=current_user.id
    )
    db.add(db_setup)
    db.commit()
    db.refresh(db_setup)
    return db_setup

@router.put("/", response_model=UserSetupConfigResponse)
def update_user_setup(
    setup: UserSetupConfigCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_setup = db.query(UserSetupConfig).filter(UserSetupConfig.user_id == current_user.id).first()
    if not db_setup:
        raise HTTPException(status_code=404, detail="User setup not found")
    
    for key, value in setup.dict().items():
        setattr(db_setup, key, value)
    
    db.commit()
    db.refresh(db_setup)
    return db_setup

@router.put("/complete")
def complete_user_setup(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_setup = db.query(UserSetupConfig).filter(UserSetupConfig.user_id == current_user.id).first()
    if not db_setup:
        raise HTTPException(status_code=404, detail="User setup not found")
    
    db_setup.is_completed = True
    db.commit()
    
    return {"message": "User setup completed successfully"}