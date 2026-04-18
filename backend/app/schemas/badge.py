from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

# Représente le badge en lui-même (l'image, le nom)
class BadgeRead(BaseModel):
    id: UUID
    name: str
    description: str
    icon_url: str | None

    model_config = ConfigDict(from_attributes=True)

# Représente l'obtention du badge par le joueur (avec la date)
class UserBadgeRead(BaseModel):
    badge: BadgeRead
    earned_at: datetime

    model_config = ConfigDict(from_attributes=True)