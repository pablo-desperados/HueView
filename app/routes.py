from fastapi import APIRouter, Query
from typing import List

router = APIRouter()

@router.get("/search", response_model=str)
def search_images(
    r: int = Query(..., ge=0, le=255),
    g: int = Query(..., ge=0, le=255),
    b: int = Query(..., ge=0, le=255),
    threshold: float = Query(30.0)
):
    return "una polla"