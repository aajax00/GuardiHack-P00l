import uuid
from sqlalchemy import Column, Integer, String, Text, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import enum

class ChallengeType(enum.Enum):
    standard = "standard"  # Points fixes
    dynamic = "dynamic"    # Points dégressifs (style CTFd)

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), index=True)  # Web, Crypto, Pwn, etc.
    description = Column(Text, nullable=True)
    connection_info = Column(String(255), nullable=True)  # ex: "ssh user@host -p 2222"
    
    value = Column(Integer, default=0)  # Points actuels
    initial = Column(Integer, default=0) # Pour le calcul dynamique
    decay = Column(Integer, default=0)   # Pour le calcul dynamique
    minimum = Column(Integer, default=0) # Pour le calcul dynamique
    
    type = Column(SQLAlchemyEnum(ChallengeType), default=ChallengeType.standard)
    state = Column(String(20), default="visible")  # visible, hidden, locked
    
    # Le Flag (Le Graal)
    flag = Column(String(255), nullable=False)
    
    max_attempts = Column(Integer, default=0)  # 0 = illimité