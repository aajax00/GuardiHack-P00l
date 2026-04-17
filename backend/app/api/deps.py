from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.token import TokenData

# Le tokenUrl sert juste à dire à Swagger où aller chercher le token quand on clique sur "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# 2. Le Vigile principal
async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> User:
    # L'erreur standard si on rejette quelqu'un
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # On essaie de décoder le token avec notre clé secrète
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # On récupère l'ID de l'utilisateur (le "sub" qu'on a mis lors du login)
        user_id: str = str(payload.get("sub"))
        
        if user_id is None:
            raise credentials_exception
            
        token_data = TokenData(user_id=int(user_id))
        
    except InvalidTokenError:
        # Si le token est expiré, malformé, ou signé avec une fausse clé -> Dehors !
        raise credentials_exception

    # 3. Si le token est valide, on va chercher le vrai utilisateur en BDD
    query = select(User).where(User.id == token_data.user_id)
    result = await db.execute(query)
    user = result.scalars().first()

    if user is None:
        raise credentials_exception
        
    # On laisse passer l'utilisateur !
    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    # Le vigile classique a déjà validé le token et nous a donné le "current_user".
    # Maintenant, on vérifie si la case "is_admin" est cochée.
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, # 403: Tu es identifié, mais tu n'as pas le droit d'entrer.
            detail="Accès refusé. Vous n'avez pas les droits d'administration.",
        )
    return current_user