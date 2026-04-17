from fastapi import APIRouter, Depends
from app.models.user import User
from app.api.deps import get_current_admin_user

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