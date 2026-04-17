from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.endpoints import auth, users, admin
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter 

# Iswagger cacher en production
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Inclusion des routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

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
