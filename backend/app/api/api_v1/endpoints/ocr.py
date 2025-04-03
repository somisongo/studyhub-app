from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List

from app.core.auth import get_current_active_user
from app.db.mongodb import get_database

router = APIRouter()

@router.post("/recognize", response_model=dict)
async def recognize_text(
    file: UploadFile = File(...),
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Reconnaissance de texte à partir d'une image.
    """
    # TODO: Implémenter la reconnaissance OCR
    # Placeholder pour test
    return {
        "text": "Texte reconnu dans l'image...",
        "confidence": 0.85,
        "processing_time": 1.2
    }

@router.post("/batch", response_model=List[dict])
async def batch_recognize(
    files: List[UploadFile] = File(...),
    db = Depends(get_database),
    current_user = Depends(get_current_active_user),
):
    """
    Reconnaissance de texte sur plusieurs images.
    """
    # TODO: Implémenter la reconnaissance par lot
    # Placeholder pour test
    results = []
    for i, file in enumerate(files):
        results.append({
            "filename": file.filename,
            "text": f"Texte reconnu dans l'image {i+1}...",
            "confidence": 0.85,
            "processing_time": 1.2
        })
    return results
