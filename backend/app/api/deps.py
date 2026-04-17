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