import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.api.v1.endpoints import auth, users, admin, challenges
from app.core.limiter import limiter 

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


# --- IMPORT POUR LA BDD ---
from app.core.database import engine, Base
from app.models.user import User   
from app.models.challenge import Challenge 

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# Iswagger cacher en production
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    lifespan=lifespan
)

# CONFIGURATION CORS (Autoriser le Front-End)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", # Port classique pour React / Next.js
        "http://localhost:5173", # Port classique pour Vite (Vue / React / Svelte)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FICHIERS STATIQUES (Héberger les images)
os.makedirs("static/icons/badges", exist_ok=True) # Dossier pour les avatars
app.mount("/icons", StaticFiles(directory="static/icons"), name="icons")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Inclusion des routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(challenges.router, prefix=f"{settings.API_V1_STR}/challenges", tags=["Challenges"])

@app.get("/", tags=["System"])
@limiter.limit("5/minute") # Limite : 5 requêtes par minute sur cette route
async def root(request: Request):
    return {"message": "Silence is golden. Not Found..."}

# Route de test (Health Check) pour s'assurer que le serveur tourne
@app.get("/health", tags=["System"])
@limiter.limit("10/minute") # Limite : 10 requêtes par minute sur cette route
async def health_check(request: Request):
    return {
        "status": "online",
        "environment": settings.ENVIRONMENT,
        "project": settings.PROJECT_NAME,
        "message": "Bienvenue dans GuardiHack P00l."
    }
