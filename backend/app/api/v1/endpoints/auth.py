from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.limiter import limiter

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(request: Request, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Vérifier le fameux Pool-Code
    if user_data.pool_code != settings.POOL_CODE: # En cyber, on reste vague sur l'erreur pour ne pas aider l'attaquant
        raise HTTPException(status_code=400, detail="Inscription refusée. Code d'accès invalide.")
    
    # 2. Vérifier si l'email ou le username existe déjà
    query = select(User).where(
        or_(User.email == user_data.email, User.username == user_data.username)
    )
    result = await db.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email ou ce nom d'utilisateur est déjà utilisé."
        )
    
    # 3. Hacher le mot de passe et créer l'utilisateur
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user