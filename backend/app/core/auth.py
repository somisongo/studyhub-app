from datetime import datetime, timedelta
from typing import Any, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field

from app.core.config import settings
from app.db.mongodb import get_database

# Modèle utilisateur pour JWT
class TokenData(BaseModel):
    user_id: Optional[str] = None
    exp: Optional[datetime] = None

# Schéma de token
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Schéma utilisateur
class User(BaseModel):
    id: str = Field(..., alias="_id")
    email: EmailStr
    name: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Configuration de la sécurité
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe en clair correspond à un hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Génère un hash sécurisé pour un mot de passe en clair.
    """
    return pwd_context.hash(password)

async def get_user(db, user_id: str) -> Optional[User]:
    """
    Récupère un utilisateur par son ID depuis la base de données.
    """
    if not user_id:
        return None
    user_data = await db["users"].find_one({"_id": user_id})
    if user_data:
        return User(**user_data)
    return None

async def get_user_by_email(db, email: str) -> Optional[User]:
    """
    Récupère un utilisateur par son email depuis la base de données.
    """
    user_data = await db["users"].find_one({"email": email})
    if user_data:
        return User(**user_data)
    return None

async def authenticate_user(db, email: str, password: str) -> Optional[User]:
    """
    Authentifie un utilisateur par email et mot de passe.
    """
    user_data = await db["users"].find_one({"email": email})
    if not user_data:
        return None
    if not verify_password(password, user_data["hashed_password"]):
        return None
    return User(**user_data)

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crée un token JWT pour l'authentification.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Crée un token de rafraîchissement JWT.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_SECRET_KEY, algorithm="HS256"
    )
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_database)
) -> User:
    """
    Dépendance pour obtenir l'utilisateur actuel à partir du token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, exp=payload.get("exp"))
    except JWTError:
        raise credentials_exception
    
    # Vérifier si le token a expiré
    if token_data.exp and datetime.utcnow() > token_data.exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = await get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dépendance pour obtenir l'utilisateur actif actuel.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilisateur inactif"
        )
    return current_user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dépendance pour obtenir l'utilisateur superutilisateur actuel.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits insuffisants"
        )
    return current_user
