from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.challenge import Challenge
from app.schemas.challenge import ChallengeRead
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