from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from app.core.auth import get_current_active_user
from app.db.mongodb import get_database
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.db.mongodb import ObjectIdField, PyObjectId

# Modèles pour les cours (normalement dans un fichier séparé)
class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
    tags: List[str] = []
    color: Optional[str] = None
    icon: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    color: Optional[str] = None
    icon: Optional[str] = None

class CourseInDB(CourseBase):
    id: ObjectIdField = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )

class CourseResponse(CourseBase):
    id: str = Field(..., alias="_id")
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(populate_by_name=True)

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
async def read_courses(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère les cours de l'utilisateur.
    """
    courses = await db.courses.find({"user_id": str(current_user.id)}).skip(skip).limit(limit).to_list(limit)
    return courses

@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course: CourseCreate,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Crée un nouveau cours.
    """
    # TODO: Implémenter la logique de création
    # Placeholder pour test
    return {
        "_id": "courseid123",
        "name": course.name,
        "description": course.description,
        "tags": course.tags,
        "color": course.color,
        "icon": course.icon,
        "user_id": str(current_user.id),
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None
    }

@router.get("/{course_id}", response_model=CourseResponse)
async def read_course(
    course_id: str,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère un cours spécifique.
    """
    # TODO: Implémenter la logique de récupération
    # Placeholder pour test
    return {
        "_id": course_id,
        "name": "Nom du cours",
        "description": "Description du cours...",
        "tags": ["tag1", "tag2"],
        "color": "#4287f5",
        "icon": "book",
        "user_id": str(current_user.id),
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None
    }

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: str,
    course_update: CourseUpdate,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Met à jour un cours.
    """
    # TODO: Implémenter la logique de mise à jour
    # Placeholder pour test
    return {
        "_id": course_id,
        "name": course_update.name or "Nom du cours",
        "description": course_update.description or "Description du cours...",
        "tags": course_update.tags or ["tag1", "tag2"],
        "color": course_update.color or "#4287f5",
        "icon": course_update.icon or "book",
        "user_id": str(current_user.id),
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-02T00:00:00"
    }

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: str,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Supprime un cours.
    """
    # TODO: Implémenter la logique de suppression
    return None

@router.get("/{course_id}/notes", response_model=List[dict])  # Idéalement, utilisez un modèle approprié
async def read_course_notes(
    course_id: str,
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Récupère les notes associées à un cours.
    """
    # TODO: Implémenter la logique de récupération
    # Placeholder pour test
    return [
        {
            "_id": "note1",
            "title": "Note 1 du cours",
            "content": "Contenu...",
            "tags": ["tag1"],
            "course_id": course_id,
            "creator_id": str(current_user.id),
            "created_at": "2023-01-01T00:00:00",
            "updated_at": None,
            "version": 1
        },
        {
            "_id": "note2",
            "title": "Note 2 du cours",
            "content": "Contenu...",
            "tags": ["tag2"],
            "course_id": course_id,
            "creator_id": str(current_user.id),
            "created_at": "2023-01-02T00:00:00",
            "updated_at": None,
            "version": 1
        }
    ]
