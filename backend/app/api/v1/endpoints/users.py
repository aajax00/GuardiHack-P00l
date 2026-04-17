from fastapi import APIRouter, Depends, Request
from app.models.user import User
from app.schemas.user import UserResponse
from app.api.deps import get_current_user
from app.core.limiter import limiter

router = APIRouter()

# Remarque : on utilise "response_model=UserResponse" pour ne JAMAIS renvoyer le mot de passe hashé !
@router.get("/me", response_model=UserResponse)
@limiter.limit("20/minute")
async def read_users_me(
    request: Request, 
    current_user: User = Depends(get_current_user) # C'est ICI qu'on place le vigile !
):
    # Si le code arrive ici, c'est que le vigile a validé le token.
    return current_user