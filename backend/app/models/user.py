import uuid
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    totp_secret = Column(String(32), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    
    xp = Column(Integer, default=0)
    score = Column(Integer, default=0)
    level = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)