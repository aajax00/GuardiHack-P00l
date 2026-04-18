from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from app.models.challenge import ChallengeType

# Schéma de base
class ChallengeBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    connection_info: Optional[str] = None
    value: int
    type: ChallengeType = ChallengeType.standard
    state: str = "visible"
    max_attempts: int = 0

# Utilisé par l'Admin pour créer/modifier (inclut le Flag)
class ChallengeCreate(ChallengeBase):
    flag: str

# Ce que le Joueur voit (SÉCURISÉ : pas de flag ici)
class ChallengeRead(ChallengeBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

# Ce que l'Admin voit (Full info)
class ChallengeAdminRead(ChallengeRead):
    flag: str