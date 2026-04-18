from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from typing import List
from app.schemas.badge import UserBadgeRead

# Ce qu'on attend de l'utilisateur pour s'inscrire
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    pool_code: str

# Ce qu'on attend pour se connecter (username OU email)
class UserLogin(BaseModel):
    login_identifier: str 
    password: str

# Ce que l'API renvoie au Frontend (SANS le mot de passe !)
class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    xp: int
    score: int
    level: int
    grade: str | None = None
    is_active: bool
    is_admin: bool
    badges: List[UserBadgeRead] = []

    model_config = ConfigDict(from_attributes=True)
    
class UserPublicRead(BaseModel):
    id: UUID
    username: str
    avatar_url: str | None = None
    bio: str | None = None
    level: int
    score: int
    grade: str | None = None
    badges: List[UserBadgeRead] = [] # On inclut les badges !

    model_config = ConfigDict(from_attributes=True)