from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from uuid import UUID

from app.models.challenge import Challenge
from app.models.user import User
from app.models.solve import Solve
from app.schemas.challenge import ChallengeRead, ChallengeSubmit
from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.utils import calculate_level, get_challenge_rewards
from app.services.badge_service import check_and_award_badges

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Challenge introuvable")
        
    query_solve = select(Solve).where(Solve.user_id == current_user.id, Solve.challenge_id == challenge_id)
    result_solve = await db.execute(query_solve)
    if result_solve.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vous avez déjà validé ce challenge")
        
    if submission.flag != challenge.flag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Flag incorrect")
        
    query_first_blood = select(func.count(Solve.id)).where(Solve.challenge_id == challenge.id)
    result_fb = await db.execute(query_first_blood)
    solve_count = result_fb.scalar()
    
    is_first_blood = (solve_count == 0)
    xp_gained = get_challenge_rewards(challenge.value, is_first_blood)
        
    new_solve = Solve(user_id=current_user.id, challenge_id=challenge.id)
    db.add(new_solve)
    
    old_level = current_user.level
    current_user.xp += xp_gained
    current_user.score += challenge.value
    current_user.level = calculate_level(current_user.xp)
    
    leveled_up = current_user.level > old_level
    db.add(current_user)
    await db.commit()
    
    new_badges = await check_and_award_badges(db, current_user, challenge, is_first_blood)
    
    msg = "🩸 First Blood ! Flag Correcte, Bien joué !" if is_first_blood else "Flag Correcte et validé, Bien joué !"
    
    if new_badges:
        msg += f"Nouveau badge débloqué : {', '.join(new_badges)}"
    
    return {
        "message": msg,
        "xp_gained": xp_gained,
        "points_gained": challenge.value,
        "new_total_xp": current_user.xp,
        "new_level": current_user.level,
        "leveled_up": leveled_up,
        "first_blood": is_first_blood,
        "unlocked_badges": new_badges
    }