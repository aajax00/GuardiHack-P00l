from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from typing import Optional

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
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes=True)