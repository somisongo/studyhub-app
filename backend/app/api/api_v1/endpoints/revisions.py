from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, ConfigDict

from app.core.auth import get_current_active_user
from app.db.mongodb import get_database, ObjectIdField, PyObjectId

# Modèles pour les révisions
class RevisionBase(BaseModel):
    note_id: str
    scheduled_date: datetime
    status: str = "pending"  # pending, completed, missed
    difficulty: Optional[int] = None  # 1-5, plus la valeur est élevée, plus c'était difficile

class RevisionCreate(RevisionBase):
    pass

class RevisionUpdate(BaseModel):
    scheduled_date: Optional[datetime] = None
    status: Optional[str] = None
    difficulty: Optional[int] = None
    feedback: Optional[str] = None

class RevisionInDB(RevisionBase):
    id: ObjectIdField = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    feedback: Optional[str] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )

class RevisionResponse(RevisionBase):
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    feedback: Optional[str] = None
    
    model_config = ConfigDict(populate_by_name=True)

router = APIRouter()

@router.get("/", response_model=List[RevisionResponse])
async def read_revisions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère les révisions de l'utilisateur.
    """
    # Construction du filtre
    filter_query = {"user_id": str(current_user.id)}
    
    if status:
        filter_query["status"] = status
    
    # Récupération des révisions
    revisions = await db.revisions.find(filter_query).skip(skip).limit(limit).to_list(limit)
    return revisions

@router.post("/", response_model=RevisionResponse, status_code=status.HTTP_201_CREATED)
async def create_revision(
    revision: RevisionCreate,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Crée une nouvelle révision programmée.
    """
    # TODO: Implémenter la logique de création
    # Placeholder pour test
    return {
        "_id": "revisionid123",
        "note_id": revision.note_id,
        "scheduled_date": revision.scheduled_date,
        "status": revision.status,
        "difficulty": revision.difficulty,
        "user_id": str(current_user.id),
        "created_at": datetime.utcnow(),
        "completed_at": None,
        "feedback": None
    }

@router.get("/due", response_model=List[RevisionResponse])
async def read_due_revisions(
    days: int = 1,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère les révisions prévues pour les N prochains jours.
    """
    # TODO: Implémenter la logique de récupération
    # Placeholder pour test
    due_date = datetime.utcnow() + timedelta(days=days)
    
    return [
        {
            "_id": "revision1",
            "note_id": "note1",
            "scheduled_date": datetime.utcnow() + timedelta(hours=4),
            "status": "pending",
            "difficulty": None,
            "user_id": str(current_user.id),
            "created_at": datetime.utcnow() - timedelta(days=1),
            "completed_at": None,
            "feedback": None
        },
        {
            "_id": "revision2",
            "note_id": "note2",
            "scheduled_date": datetime.utcnow() + timedelta(days=1),
            "status": "pending",
            "difficulty": None,
            "user_id": str(current_user.id),
            "created_at": datetime.utcnow() - timedelta(days=2),
            "completed_at": None,
            "feedback": None
        }
    ]

@router.put("/{revision_id}", response_model=RevisionResponse)
async def update_revision(
    revision_id: str,
    revision_update: RevisionUpdate,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Met à jour une révision (marquer comme terminée, reporter, etc.).
    """
    # TODO: Implémenter la logique de mise à jour
    # Placeholder pour test
    completed_at = None
    if revision_update.status == "completed":
        completed_at = datetime.utcnow()
        
    return {
        "_id": revision_id,
        "note_id": "note1",
        "scheduled_date": revision_update.scheduled_date or (datetime.utcnow() + timedelta(hours=4)),
        "status": revision_update.status or "pending",
        "difficulty": revision_update.difficulty or 3,
        "user_id": str(current_user.id),
        "created_at": datetime.utcnow() - timedelta(days=1),
        "completed_at": completed_at,
        "feedback": revision_update.feedback or None
    }

@router.delete("/{revision_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_revision(
    revision_id: str,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Supprime une révision programmée.
    """
    # TODO: Implémenter la logique de suppression
    return None

@router.post("/generate", response_model=List[RevisionResponse])
async def generate_revision_schedule(
    note_id: str,
    count: int = 5,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Génère un programme de révision basé sur la courbe de l'oubli.
    """
    # TODO: Implémenter la logique de génération
    # Placeholder pour test
    revisions = []
    intervals = [1, 3, 7, 14, 30]  # Intervalles en jours selon la courbe de l'oubli
    
    for i in range(min(count, len(intervals))):
        revisions.append({
            "_id": f"revision{i+1}",
            "note_id": note_id,
            "scheduled_date": datetime.utcnow() + timedelta(days=intervals[i]),
            "status": "pending",
            "difficulty": None,
            "user_id": str(current_user.id),
            "created_at": datetime.utcnow(),
            "completed_at": None,
            "feedback": None
        })
    
    return revisions
