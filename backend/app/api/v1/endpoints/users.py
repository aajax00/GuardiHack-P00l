from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.models.user import User
from app.models.challenge import Challenge
from app.models.solve import Solve
from app.schemas.user import UserResponse
from app.api.deps import get_current_user
from app.core.limiter import limiter
from app.core.database import get_db
from app.core.utils import get_grade

router = APIRouter()

# Remarque : on utilise "response_model=UserResponse" pour ne JAMAIS renvoyer le mot de passe hashé !
@router.get("/me", response_model=UserResponse)
@limiter.limit("20/minute")
async def read_users_me(
    request: Request, 
    current_user: User = Depends(get_current_user) # C'est ICI qu'on place le vigile !
):
    user_data = current_user.__dict__.copy()
    user_data["grade"] = get_grade(current_user.level)
    return user_data

@router.get("/scoreboard")
@limiter.limit("10/minute")
async def get_scoreboard(request: Request, db: AsyncSession = Depends(get_db)):
    # 1. Classement Global (Top 100)
    query_global = select(User).where(User.score > 0).order_by(User.score.desc())
    result_global = await db.execute(query_global)
    users_global = result_global.scalars().all()
    
    global_board = []
    for rank, u in enumerate(users_global, start=1):
        global_board.append({
            "rank": rank,
            "username": u.username,
            "score": u.score,
            "level": u.level,
            "grade": get_grade(u.level)
        })

    # 2. Classement par Catégorie (Jointure massive Solve + Challenge + User)
    query_categories = (
        select(
            User.username,
            Challenge.category,
            func.sum(Challenge.value).label("category_score")
        )
        .select_from(Solve)
        .join(Challenge, Solve.challenge_id == Challenge.id)
        .join(User, Solve.user_id == User.id)
        .group_by(User.username, Challenge.category)
        .order_by(Challenge.category, func.sum(Challenge.value).desc())
    )
    result_categories = await db.execute(query_categories)
    
    # On reformate les données pour que le Front-End puisse les lire facilement
    categories_board = {}
    for row in result_categories.fetchall():
        cat = row.category
        if cat not in categories_board:
            categories_board[cat] = []
            
        rank_in_cat = len(categories_board[cat]) + 1
        
        categories_board[cat].append({
            "rank": rank_in_cat,
            "username": row.username,
            "score": row.category_score
        })

    return {
        "total_active_players": len(global_board),
        "global": global_board,
        "by_category": categories_board
    }