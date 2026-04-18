from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from app.models.challenge import Challenge
from app.models.user import User
from app.models.solve import Solve
from app.schemas.challenge import ChallengeRead, ChallengeSubmit
from app.api.deps import get_current_user
from app.core.database import get_db

router = APIRouter()

@router.get("/", response_model=List[ChallengeRead])
async def list_visible_challenges(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = select(Challenge).where(Challenge.state == "visible")
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/{challenge_id}/submit")
async def submit_flag(
    challenge_id: UUID,
    submission: ChallengeSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query_chal = select(Challenge).where(Challenge.id == challenge_id, Challenge.state == "visible")
    result_chal = await db.execute(query_chal)
    challenge = result_chal.scalars().first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge introuvable"
        )
        
    query_solve = select(Solve).where(Solve.user_id == current_user.id, Solve.challenge_id == challenge_id)
    result_solve = await db.execute(query_solve)
    if result_solve.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vous avez déjà validé ce challenge"
        )
        
    if submission.flag != challenge.flag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Flag incorrect"
        )
        
    new_solve = Solve(user_id=current_user.id, challenge_id=challenge.id)
    db.add(new_solve)
    
    current_user.xp += challenge.value
    current_user.score += challenge.value
    db.add(current_user)
    
    await db.commit()
    
    return {
        "message": "Flag Correcte et validé, Bien joué !",
        "xp_gained": challenge.value,
        "new_total_xp": current_user.xp
    }