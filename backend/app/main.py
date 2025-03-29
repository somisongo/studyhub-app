from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.auth import get_current_user

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API pour l'application StudyHub de prise de notes intelligente",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuration CORS
origins = [
    settings.FRONTEND_URL,
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Santé"])
async def root():
    """
    Endpoint de santé de l'API.
    Permet de vérifier que l'API est opérationnelle.
    """
    return {"message": "Bienvenue sur l'API StudyHub", "status": "online"}

@app.get("/health", tags=["Santé"])
async def health_check():
    """
    Endpoint de vérification de l'état de santé.
    Utilisé par Kubernetes pour les health checks.
    """
    return {"status": "healthy"}

@app.get("/ready", tags=["Santé"])
async def readiness_check():
    """
    Endpoint de vérification de disponibilité.
    Utilisé par Kubernetes pour les readiness checks.
    """
    return {"status": "ready"}

@app.get("/me", tags=["Utilisateur"])
async def read_current_user(current_user = Depends(get_current_user)):
    """
    Endpoint pour récupérer les informations de l'utilisateur connecté.
    """
    return current_user

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Gestionnaire d'exceptions HTTP personnalisé.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
