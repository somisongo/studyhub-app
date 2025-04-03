from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr

from app.core.auth import get_current_active_user
from app.db.mongodb import get_database, ObjectIdField, PyObjectId

# Modèles pour les partages
class ShareBase(BaseModel):
    note_id: str
    permissions: str = "read"  # read, edit
    target_email: Optional[EmailStr] = None
    target_user_id: Optional[str] = None
    expiration_date: Optional[datetime] = None
    message: Optional[str] = None

class ShareCreate(ShareBase):
    pass

class ShareUpdate(BaseModel):
    permissions: Optional[str] = None
    expiration_date: Optional[datetime] = None
    active: Optional[bool] = None

class ShareInDB(ShareBase):
    id: ObjectIdField = Field(default_factory=PyObjectId, alias="_id")
    source_user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    active: bool = True
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )

class ShareResponse(ShareBase):
    id: str = Field(..., alias="_id")
    source_user_id: str
    created_at: datetime
    active: bool
    
    model_config = ConfigDict(populate_by_name=True)

router = APIRouter()

@router.get("/", response_model=List[ShareResponse])
async def read_shared_by_me(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère les notes partagées par l'utilisateur.
    """
    # Construction du filtre
    filter_query = {"source_user_id": str(current_user.id)}
    
    if active_only:
        filter_query["active"] = True
    
    # Récupération des partages
    shares = await db.shares.find(filter_query).skip(skip).limit(limit).to_list(limit)
    return shares

@router.get("/shared-with-me", response_model=List[ShareResponse])
async def read_shared_with_me(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère les notes partagées avec l'utilisateur.
    """
    # Construction du filtre
    filter_query = {
        "$or": [
            {"target_user_id": str(current_user.id)},
            {"target_email": current_user.email}
        ]
    }
    
    if active_only:
        filter_query["active"] = True
    
    # Récupération des partages
    shares = await db.shares.find(filter_query).skip(skip).limit(limit).to_list(limit)
    return shares

@router.post("/", response_model=ShareResponse, status_code=status.HTTP_201_CREATED)
async def create_share(
    share: ShareCreate,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Partage une note avec un autre utilisateur.
    """
    # Vérifier si l'utilisateur est propriétaire de la note
    note = await db.notes.find_one({"_id": share.note_id})
    if not note or note.get("creator_id") != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez partager que vos propres notes"
        )
    
    # TODO: Implémenter la logique de partage
    # Placeholder pour test
    return {
        "_id": "shareid123",
        "note_id": share.note_id,
        "permissions": share.permissions,
        "target_email": share.target_email,
        "target_user_id": share.target_user_id,
        "expiration_date": share.expiration_date,
        "message": share.message,
        "source_user_id": str(current_user.id),
        "created_at": datetime.utcnow(),
        "active": True
    }

@router.put("/{share_id}", response_model=ShareResponse)
async def update_share(
    share_id: str,
    share_update: ShareUpdate,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Met à jour les paramètres d'un partage.
    """
    # Vérifier si l'utilisateur est propriétaire du partage
    share = await db.shares.find_one({"_id": share_id})
    if not share or share.get("source_user_id") != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez modifier que vos propres partages"
        )
    
    # TODO: Implémenter la logique de mise à jour
    # Placeholder pour test
    return {
        "_id": share_id,
        "note_id": "note123",
        "permissions": share_update.permissions or "read",
        "target_email": "user@example.com",
        "target_user_id": None,
        "expiration_date": share_update.expiration_date,
        "message": "Voici mes notes partagées",
        "source_user_id": str(current_user.id),
        "created_at": datetime.utcnow() - timedelta(days=1),
        "active": share_update.active if share_update.active is not None else True
    }

@router.delete("/{share_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_share(
    share_id: str,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Supprime un partage.
    """
    # Vérifier si l'utilisateur est propriétaire du partage
    share = await db.shares.find_one({"_id": share_id})
    if not share or share.get("source_user_id") != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez supprimer que vos propres partages"
        )
    
    # TODO: Implémenter la logique de suppression
    return None
