from sqlalchemy import Column, Integer, String, Text, JSON, Boolean
from app.core.database import Base

class MuscleGroup(Base):
    __tablename__ = "muscle_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=False)
    description = Column(Text)
    color = Column(String)  # Hex color for UI
    muscle_names = Column(JSON)  # List of muscle names in this group
    is_primary = Column(Boolean, default=False)  # Primary vs secondary muscle groups