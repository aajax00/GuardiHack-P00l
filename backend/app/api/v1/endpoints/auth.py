from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_password_hash
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.limiter import limiter
from app.schemas.token import Token
from datetime import timedelta

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

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")  # On protège aussi le login contre le bruteforce !
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(
        or_(User.email == form_data.username, User.username == form_data.username)
    )
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email/Pseudo ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Créer le Token (le fameux badge)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # On met l'ID de l'utilisateur dans le "sub" (subject) du token. 
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}