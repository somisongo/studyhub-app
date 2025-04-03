from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.core.auth import get_current_active_user
from app.models.user import UserCreate, UserInDB, UserResponse, UserUpdate
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """
    Récupère la liste des utilisateurs.
    """
    # Vérifier si l'utilisateur est un super-utilisateur
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission insuffisante"
        )
    
    users = await db.users.find().skip(skip).limit(limit).to_list(limit)
    return users

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: UserInDB = Depends(get_current_active_user),
):
    """
    Récupère les informations de l'utilisateur connecté.
    """
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    db = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """
    Récupère les informations d'un utilisateur spécifique.
    """
    # Vérifier si l'utilisateur est un super-utilisateur ou consulte son propre profil
    if not current_user.is_superuser and str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission insuffisante"
        )
    
    user = await db.users.find_one({"_id": user_id})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """
    Met à jour les informations d'un utilisateur.
    """
    # Vérifier si l'utilisateur est un super-utilisateur ou modifie son propre profil
    if not current_user.is_superuser and str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission insuffisante"
        )
    
    # TODO: Implémenter la logique de mise à jour
    # Placeholder pour test
    return {"_id": user_id, "email": "user@example.com", "name": "User", "is_active": True, "is_superuser": False, "created_at": "2023-01-01T00:00:00"}

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    db = Depends(get_database),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """
    Supprime un utilisateur.
    """
    # Vérifier si l'utilisateur est un super-utilisateur
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission insuffisante"
        )
    
    # TODO: Implémenter la logique de suppression
    return None
