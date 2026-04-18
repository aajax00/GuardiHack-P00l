from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.challenge import Challenge
from app.schemas.challenge import ChallengeCreate, ChallengeAdminRead
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
@router.post("/challenges", response_model=ChallengeAdminRead)
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
    result = await db.execute(select(Challenge))
    return result.scalars().all()