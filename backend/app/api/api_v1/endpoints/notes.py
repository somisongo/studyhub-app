from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.core.auth import get_current_active_user
from app.models.note import NoteCreate, NoteInDB, NoteResponse, NoteUpdate, NoteFilter
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/", response_model=List[NoteResponse])
async def read_notes(
    skip: int = 0,
    limit: int = 100,
    course_id: Optional[str] = None,
    tag: Optional[str] = None,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère les notes de l'utilisateur avec filtrage optionnel.
    """
    # Construction du filtre
    filter_query = {"creator_id": str(current_user.id), "is_deleted": False}
    
    if course_id:
        filter_query["course_id"] = course_id
    
    if tag:
        filter_query["tags"] = tag
    
    # Récupération des notes
    notes = await db.notes.find(filter_query).skip(skip).limit(limit).to_list(limit)
    return notes

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Crée une nouvelle note.
    """
    # TODO: Implémenter la logique de création
    # Placeholder pour test
    return {
        "_id": "noteid123",
        "title": note.title,
        "content": note.content,
        "tags": note.tags,
        "course_id": note.course_id,
        "creator_id": str(current_user.id),
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None,
        "version": 1
    }

@router.get("/{note_id}", response_model=NoteResponse)
async def read_note(
    note_id: str,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère une note spécifique.
    """
    # TODO: Implémenter la logique de récupération
    # Placeholder pour test
    return {
        "_id": note_id,
        "title": "Titre de la note",
        "content": "Contenu de la note...",
        "tags": ["tag1", "tag2"],
        "course_id": "course123",
        "creator_id": str(current_user.id),
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None,
        "version": 1
    }

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Met à jour une note.
    """
    # TODO: Implémenter la logique de mise à jour
    # Placeholder pour test
    return {
        "_id": note_id,
        "title": note_update.title or "Titre de la note",
        "content": note_update.content or "Contenu de la note...",
        "tags": note_update.tags or ["tag1", "tag2"],
        "course_id": note_update.course_id or "course123",
        "creator_id": str(current_user.id),
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-02T00:00:00",
        "version": 2
    }

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: str,
    permanent: bool = False,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Supprime une note (mise en corbeille ou suppression permanente).
    """
    # TODO: Implémenter la logique de suppression
    return None

@router.post("/search", response_model=List[NoteResponse])
async def search_notes(
    filter_params: NoteFilter,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Recherche de notes avec des critères avancés.
    """
    # TODO: Implémenter la logique de recherche
    # Placeholder pour test
    return [
        {
            "_id": "note1",
            "title": "Titre de la note 1",
            "content": "Contenu de la note 1...",
            "tags": ["tag1"],
            "course_id": "course123",
            "creator_id": str(current_user.id),
            "created_at": "2023-01-01T00:00:00",
            "updated_at": None,
            "version": 1
        },
        {
            "_id": "note2",
            "title": "Titre de la note 2",
            "content": "Contenu de la note 2...",
            "tags": ["tag2"],
            "course_id": "course123",
            "creator_id": str(current_user.id),
            "created_at": "2023-01-02T00:00:00",
            "updated_at": None,
            "version": 1
        }
    ]
