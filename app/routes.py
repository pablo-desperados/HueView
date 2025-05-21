import logging
from typing import Dict, List
from indexer import indexer
from fastapi import APIRouter, BackgroundTasks, Depends
from models import WikiImage, get_db
from sqlalchemy import func
from sqlalchemy.orm import Session
from collector import collect_images_task, is_collector_running

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def root():
    return {"status": "running"}

@router.get("/start-scraping")
async def start_scraping(background_tasks: BackgroundTasks):
    if is_collector_running:
        return {"status": "already_running", "message": "Image collector is already running"}
    else:
        background_tasks.add_task(collect_images_task)
        return {"status": "started", "message": "Image collector started"}

@router.post("/index/build")
async def build_index(force_rebuild: bool = False):
    """Build or rebuild the KD-tree index"""
    # This will trigger analysis of any unanalyzed images
    await indexer.build_index(force_rebuild=force_rebuild)
    return {"status": "success", "message": "Index built successfully"}
