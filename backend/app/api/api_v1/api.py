from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, notes, courses, ocr, nlp, revisions, shares

api_router = APIRouter()

# Routes d'authentification
api_router.include_router(auth.router, prefix="/auth", tags=["Authentification"])

# Routes utilisateurs
api_router.include_router(users.router, prefix="/users", tags=["Utilisateurs"])

# Routes notes
api_router.include_router(notes.router, prefix="/notes", tags=["Notes"])

# Routes cours
api_router.include_router(courses.router, prefix="/courses", tags=["Cours"])

# Routes OCR
api_router.include_router(ocr.router, prefix="/ocr", tags=["OCR"])

# Routes NLP
api_router.include_router(nlp.router, prefix="/nlp", tags=["NLP"])

# Routes révisions
api_router.include_router(revisions.router, prefix="/revisions", tags=["Révisions"])

# Routes partages
api_router.include_router(shares.router, prefix="/shares", tags=["Partages"])
