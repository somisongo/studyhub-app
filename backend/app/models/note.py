from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field, ConfigDict

from app.db.mongodb import PyObjectId


class NoteBase(BaseModel):
    """
    Modèle de base pour les notes.
    """
    title: str
    content: str
    tags: List[str] = []
    course_id: Optional[str] = None
    metadata: Dict[str, Any] = {}


class NoteCreate(NoteBase):
    """
    Modèle pour la création d'une note.
    """
    pass


class NoteUpdate(BaseModel):
    """
    Modèle pour la mise à jour d'une note.
    """
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    course_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class NoteInDB(NoteBase):
    """
    Modèle de la note en base de données.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creator_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    version: int = 1
    is_deleted: bool = False

    # Configuration compatible avec Pydantic v2
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )

    # Pour rétrocompatibilité avec Pydantic v1
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class NoteResponse(NoteBase):
    """
    Modèle de réponse pour les informations de note.
    """
    id: str = Field(..., alias="_id")
    creator_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    version: int
    
    # Configuration compatible avec Pydantic v2
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    # Pour rétrocompatibilité avec Pydantic v1
    class Config:
        allow_population_by_field_name = True


class NoteWithSummary(NoteResponse):
    """
    Note avec résumé automatique.
    """
    summary: str
    key_concepts: List[str] = []


class NoteVersion(BaseModel):
    """
    Version d'une note pour l'historique.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    note_id: str
    content: str
    title: str
    version: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str
    
    # Configuration compatible avec Pydantic v2
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
    
    # Pour rétrocompatibilité avec Pydantic v1
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}


class NoteFilter(BaseModel):
    """
    Filtre pour la recherche de notes.
    """
    text: Optional[str] = None
    tags: Optional[List[str]] = None
    course_id: Optional[str] = None
    creator_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class MediaItem(BaseModel):
    """
    Élément multimédia attaché à une note.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    note_id: str
    type: str  # 'image', 'audio', 'video', 'pdf'
    url: str
    filename: str
    mimetype: str
    size: int
    transcription: Optional[str] = None
    position: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Configuration compatible avec Pydantic v2
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={PyObjectId: str}
    )
    
    # Pour rétrocompatibilité avec Pydantic v1
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {PyObjectId: str}
