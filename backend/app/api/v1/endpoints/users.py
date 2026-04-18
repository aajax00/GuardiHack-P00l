from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from uuid import UUID

from app.models.user import User
from app.models.challenge import Challenge
from app.models.solve import Solve
from app.models.badge import Badge, UserBadge
from app.schemas.user import UserResponse, UserPublicRead
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_data = current_user.__dict__.copy()
    user_data["grade"] = get_grade(current_user.level)
    
    query_badges = (
        select(Badge, UserBadge.earned_at)
        .join(UserBadge, Badge.id == UserBadge.badge_id)
        .where(UserBadge.user_id == current_user.id)
    )
    result_badges = await db.execute(query_badges)
    
    badges_list = []
    for badge, earned_at in result_badges.all():
        badges_list.append({
            "badge": {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "icon_url": badge.icon_url
            },
            "earned_at": earned_at
        })
        
    user_data["badges"] = badges_list
    return user_data

@router.get("/{user_id}", response_model=UserPublicRead)
async def get_public_profile(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    # 1. On cherche l'utilisateur
    query = select(User).where(User.id == user_id)
    user = (await db.execute(query)).scalars().first()
    
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    user_data = user.__dict__.copy()
    user_data["grade"] = get_grade(user.level)
    
    # 2. On récupère ses badges (comme pour la route /me)
    query_badges = (
        select(Badge, UserBadge.earned_at)
        .join(UserBadge, Badge.id == UserBadge.badge_id)
        .where(UserBadge.user_id == user_id)
    )
    result_badges = await db.execute(query_badges)
    
    badges_list = []
    for badge, earned_at in result_badges.all():
        badges_list.append({
            "badge": {
                "id": badge.id,
                "name": badge.name,
                "description": badge.description,
                "icon_url": badge.icon_url
            },
            "earned_at": earned_at
        })
        
    user_data["badges"] = badges_list
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