from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.db.mongodb import PyObjectId


class UserBase(BaseModel):
    """
    Modèle de base pour les informations utilisateur.
    """
    email: EmailStr
    name: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    """
    Modèle pour la création d'un utilisateur.
    """
    password: str


class UserUpdate(BaseModel):
    """
    Modèle pour la mise à jour d'un utilisateur.
    """
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserInDB(UserBase):
    """
    Modèle de l'utilisateur en base de données.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    preferences: dict = {}

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class UserResponse(UserBase):
    """
    Modèle de réponse pour les informations utilisateur.
    """
    id: str = Field(..., alias="_id")
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
