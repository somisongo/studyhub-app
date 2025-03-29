from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    get_user_by_email,
    Token,
    User,
)
from app.core.config import settings
from app.db.mongodb import get_database
from app.models.user import UserCreate, UserInDB
from pydantic import EmailStr

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_access_token(
    db = Depends(get_database),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Obtenir un token JWT pour l'authentification.
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "refresh_token": create_refresh_token(user.id, expires_delta=refresh_token_expires),
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str = Body(...),
    db = Depends(get_database)
) -> Any:
    """
    Rafraîchir le token d'accès.
    """
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_SECRET_KEY, algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "access_token": create_access_token(user.id, expires_delta=access_token_expires),
        "refresh_token": create_refresh_token(user.id, expires_delta=refresh_token_expires),
        "token_type": "bearer",
    }

@router.post("/register", response_model=User)
async def register_user(
    *,
    db = Depends(get_database),
    user_in: UserCreate
) -> Any:
    """
    Créer un nouveau compte utilisateur.
    """
    user = await get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte avec cet email existe déjà",
        )
    
    # Création de l'utilisateur
    user_in_db = UserInDB(
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password),
    )
    
    # Insertion dans la base de données
    result = await db["users"].insert_one(user_in_db.dict(exclude_none=True, by_alias=True))
    
    # Récupération de l'utilisateur créé
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    
    return User(**created_user)

@router.post("/reset-password-request")
async def reset_password_request(
    email: EmailStr = Body(...),
    db = Depends(get_database)
) -> Any:
    """
    Demande de réinitialisation de mot de passe.
    """
    user = await get_user_by_email(db, email=email)
    if not user:
        # Ne pas révéler que l'email n'existe pas pour des raisons de sécurité
        return {"msg": "Un email de réinitialisation a été envoyé si l'adresse existe"}
    
    # TODO: Implémenter l'envoi d'email avec un token de réinitialisation
    # Ici, nous envoyons un email fictif pour la démonstration
    
    return {"msg": "Un email de réinitialisation a été envoyé"}
