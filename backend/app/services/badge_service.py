from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.badge import Badge, UserBadge
from app.models.solve import Solve
from app.models.user import User
from app.models.challenge import Challenge

async def check_and_award_badges(db: AsyncSession, user: User, challenge: Challenge, is_first_blood: bool) -> list[str]:
    new_badges_names = []

    # Fonction utilitaire 1 : Récupérer ou créer un badge dans la base
    async def get_or_create_badge(name: str, description: str, icon: str):
        query = select(Badge).where(Badge.name == name)
        badge = (await db.execute(query)).scalars().first()
        if not badge:
            badge = Badge(name=name, description=description, icon_url=icon)
            db.add(badge)
            await db.commit()
            await db.refresh(badge)
        return badge

    # Fonction utilitaire 2 : Attribuer un badge simple (qui s'accumule)
    async def award_simple(badge_name: str, description: str, icon: str):
        badge = await get_or_create_badge(badge_name, description, icon)
        query_ub = select(UserBadge).where(UserBadge.user_id == user.id, UserBadge.badge_id == badge.id)
        if not (await db.execute(query_ub)).scalars().first():
            db.add(UserBadge(user_id=user.id, badge_id=badge.id))
            new_badges_names.append(badge.name)

    # ==========================================
    # 1. BADGES D'ACTIONS (S'accumulent)
    # ==========================================

    if is_first_blood:
        await award_simple("0day Exploit", "Premier sang ! A compromis un système avant tout le monde.", "/icons/badges/first_blood.png")

    query_solves = select(func.count(Solve.id)).where(Solve.user_id == user.id)
    solve_count = (await db.execute(query_solves)).scalar() or 0

    query_total_chals = select(func.count(Challenge.id)).where(Challenge.state == "visible")
    total_chals = (await db.execute(query_total_chals)).scalar() or 0

    if total_chals > 0 and solve_count == total_chals:
        await award_simple("Pwn All The Things", "Système compromis à 100%. A validé TOUS les challenges visibles.", "/icons/badges/completionist.png")

    if solve_count == 1:
        await award_simple("Hello World", "A validé son tout premier challenge.", "/icons/badges/hello.png")
    if solve_count == 10:
        await award_simple("Machine", "A validé 10 challenges.", "/icons/badges/machine.png")

    # ==========================================
    # 2. BADGES DE CLASSEMENT (Meilleur historique uniquement)
    # ==========================================
    
    # On définit les paliers du meilleur (index 0) au moins bon (index 5)
    rank_tiers = [
        {"name": "God Mode", "limit": 1, "desc": "A atteint la 1ère place globale", "icon": "/icons/badges/top1.png"},
        {"name": "APT", "limit": 3, "desc": "A fait partie du TOP 3", "icon": "/icons/badges/top3.png"},
        {"name": "Black Hat", "limit": 10, "desc": "A fait partie du TOP 10", "icon": "/icons/badges/top10.png"},
        {"name": "Red Teamer", "limit": 50, "desc": "A fait partie du TOP 50", "icon": "/icons/badges/top50.png"},
        {"name": "White Hat", "limit": 100, "desc": "A fait partie du TOP 100", "icon": "/icons/badges/top100.png"},
        {"name": "Ping Sweeper", "limit": 500, "desc": "A fait partie du TOP 500", "icon": "/icons/badges/top500.png"}
    ]

    # On calcule son rang exact à l'instant T
    query_rank = select(func.count(User.id)).where(User.score > user.score)
    current_rank = ((await db.execute(query_rank)).scalar() or 0) + 1

    # On trouve à quel palier il a droit avec son rang actuel
    qualified_tier = None
    qualified_index = 999  # 999 = Pas de rang

    for i, tier in enumerate(rank_tiers):
        if current_rank <= tier["limit"]:
            qualified_tier = tier
            qualified_index = i
            break  # On s'arrête au premier trouvé car la liste va du meilleur au pire

    if qualified_tier:
        # On va chercher tous les badges de classement existants dans la BDD
        rank_badge_names = [t["name"] for t in rank_tiers]
        query_all_ranks = select(Badge).where(Badge.name.in_(rank_badge_names))
        db_rank_badges = (await db.execute(query_all_ranks)).scalars().all()
        
        # On regarde lesquels le joueur possède déjà
        query_user_ranks = select(UserBadge).where(
            UserBadge.user_id == user.id,
            UserBadge.badge_id.in_([b.id for b in db_rank_badges]) if db_rank_badges else False
        )
        user_current_rank_badges = (await db.execute(query_user_ranks)).scalars().all()
        
        # On cherche le "meilleur" (l'index le plus bas) badge de classement que le joueur possède déjà
        best_owned_index = 999
        for ub in user_current_rank_badges:
            # On retrouve le nom du badge à partir de son ID
            badge_name = next((b.name for b in db_rank_badges if b.id == ub.badge_id), None)
            if badge_name:
                # On trouve son index dans notre liste de paliers
                tier_index = next((i for i, t in enumerate(rank_tiers) if t["name"] == badge_name), 999)
                if tier_index < best_owned_index:
                    best_owned_index = tier_index

        # MAGIE ICI : Si le niveau pour lequel il se qualifie (qualified_index) 
        # est MEILLEUR (plus petit) que son meilleur badge actuel (best_owned_index)
        if qualified_index < best_owned_index:
            
            # 1. On supprime tous ses anciens badges de classement pour faire de la place
            for ub in user_current_rank_badges:
                await db.delete(ub)
                
            # 2. On lui donne le nouveau badge tout beau tout neuf
            new_badge_db = await get_or_create_badge(
                qualified_tier["name"], 
                qualified_tier["desc"], 
                qualified_tier["icon"]
            )
            db.add(UserBadge(user_id=user.id, badge_id=new_badge_db.id))
            new_badges_names.append(qualified_tier["name"])

    # On sauvegarde tout ce qui a été modifié dans la base de données
    if new_badges_names or (qualified_tier and qualified_index < best_owned_index):
        await db.commit()

    return new_badges_names