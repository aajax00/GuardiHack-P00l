from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from app.models.challenge import Challenge
from app.schemas.challenge import ChallengeCreate, ChallengeAdminRead, ChallengeUpdate
from app.models.user import User
from app.api.deps import get_current_admin_user
from app.core.database import get_db

router = APIRouter()

# On place le Super-Vigile ici !
@router.get("/dashboard")
async def read_admin_dashboard(
    current_admin: User = Depends(get_current_admin_user)
):
    return {
        "message": f"Bienvenue dans la P00l secrete, Maitre nageur {current_admin.username}.",
        "admin_status": "Actif",
        "actions_disponibles": ["Créer un défi", "Bannir un utilisateur"] # C'est factice pour l'instant
    }
    
# --- ROUTES CHALLENGES (ADMIN ONLY) ---
@router.post("/challenges", response_model=ChallengeAdminRead, status_code=status.HTTP_201_CREATED)
async def create_challenge(
    challenge_in: ChallengeCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    new_challenge = Challenge(**challenge_in.model_dump())
    db.add(new_challenge)
    await db.commit()
    await db.refresh(new_challenge)
    return new_challenge

@router.get("/challenges", response_model=List[ChallengeAdminRead])
async def list_challenges_admin(
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    result = await db.execute(select(Challenge).order_by(Challenge.category, Challenge.value))
    return result.scalars().all()

@router.patch("/challenges/{challenge_id}", response_model=ChallengeAdminRead)
async def update_challenge(
    challenge_id: UUID,
    challenge_in: ChallengeUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    query = select(Challenge).where(Challenge.id == challenge_id)
    result = await db.execute(query)
    challenge = result.scalars().first()
    
    if not challenge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge Introuvable")
    
    update_data = challenge_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(challenge, field, value)
        
    db.add(challenge)
    await db.commit()
    await db.refresh(challenge)
    return challenge

@router.delete("/challenges/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_challenge(
    challenge_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    query = select(Challenge).where(Challenge.id == challenge_id)
    result = await db.execute(query)
    challenge = result.scalars().first()

    if not challenge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge Introuvable")

    await db.delete(challenge)
    await db.commit()