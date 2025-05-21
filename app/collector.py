import asyncio
import logging
import os
import random
from typing import Dict, List

import httpx
from models import SessionLocal, WikiImage
from sqlalchemy import func
from sqlalchemy.orm import Session

IMAGE_DIRECTORY = "downloaded_images"
IMAGES_LIMIT = 2
images_collected = 0
is_collector_running = False
image_data = []
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

os.makedirs(IMAGE_DIRECTORY, exist_ok=True)
THEMES = {
    "places": [
        "Category:Cities_by_country", 
        "Category:National_parks", 
        "Category:World_Heritage_Sites",
        "Category:Tourist_attractions",
        "Category:Mountains"
    ],
    "animals": [
        "Category:Mammals", 
        "Category:Birds", 
        "Category:Reptiles",
        "Category:Fish",
        "Category:Amphibians"
    ]
}

async def fetch_images_from_wikipedia(category: str, limit: int = 10, db: Session = None) -> List[Dict]:
    """Fetch images from a Wikipedia category and store in the database"""
    results = []
    
    if db is None:
        db = SessionLocal()
    
    async with httpx.AsyncClient() as client:
        # Get pages in category
        params = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": category,
            "cmlimit": limit,
            "cmtype": "page"
        }
        
        try:
            response = await client.get("https://en.wikipedia.org/w/api.php", params=params)
            data = response.json()
            
            # Get page IDs
            page_ids = [str(page["pageid"]) for page in data.get("query", {}).get("categorymembers", [])]
            
            if not page_ids:
                return results
                
            # Get images for these pages
            params = {
                "action": "query",
                "format": "json",
                "prop": "images|info|imageinfo",
                "iiprop": "url|size|mime",
                "pageids": "|".join(page_ids)
            }
            
            response = await client.get("https://en.wikipedia.org/w/api.php", params=params)
            data = response.json()
            
            # Process results
            for page_id, page_data in data.get("query", {}).get("pages", {}).items():
                page_title = page_data.get("title", "Unknown")
                
                # For each image in the page
                for image in page_data.get("images", []):
                    image_title = image.get("title", "")
                    
                    # Skip non-image files and SVGs
                    if not image_title.lower().endswith(('.jpg', '.jpeg', '.png')):
                        continue
                    
                    # Get image details
                    img_params = {
                        "action": "query",
                        "format": "json",
                        "prop": "imageinfo",
                        "iiprop": "url|size|mime",
                        "titles": image_title
                    }
                    
                    img_response = await client.get("https://en.wikipedia.org/w/api.php", params=img_params)
                    img_data = img_response.json()
                    
                    # Extract image URL and info
                    for img_id, img_info in img_data.get("query", {}).get("pages", {}).items():
                        if "imageinfo" in img_info and img_info["imageinfo"]:
                            image_info = img_info["imageinfo"][0]
                            image_url = image_info.get("url", "")
                            
                            if image_url:
                                # Check if image already exists in the database
                                existing = db.query(WikiImage).filter(WikiImage.image_url == image_url).first()
                                if existing:
                                    logger.info(f"Skipping duplicate image: {image_title}")
                                    continue
                                
                                # Determine theme based on category
                                theme = "places" if any(place in category for place in THEMES["places"]) else "animals"
                                
                                # Create new image record
                                new_image = WikiImage(
                                    source_page=page_title,
                                    image_title=image_title,
                                    image_url=image_url,
                                    category=category,
                                    theme=theme,
                                    width=image_info.get("width"),
                                    height=image_info.get("height"),
                                    file_size=image_info.get("size")
                                )
                                
                                db.add(new_image)
                                db.commit()
                                db.refresh(new_image)
                                
                                results.append({
                                    "id": new_image.id,
                                    "source_page": new_image.source_page,
                                    "image_title": new_image.image_title,
                                    "image_url": new_image.image_url,
                                    "category": new_image.category,
                                    "theme": new_image.theme
                                })
        
        except Exception as e:
            logger.error(f"Error fetching from Wikipedia: {str(e)}")
            db.rollback()
            
    return results



async def collect_images_task():
    global is_collector_running
    is_collector_running = True
    logger.info(f"Target: {IMAGES_LIMIT} images")
    db = SessionLocal()
    
    try:
        current_count = db.query(func.count(WikiImage.id)).scalar()
        logger.info(f"Currently have {current_count} images in database")
        while current_count < IMAGES_LIMIT and is_collector_running:
            theme = random.choice(["places", "animals"])
            category = random.choice(THEMES[theme])
            logger.info(f"Fetching from category: {category}")
            batch_size = min(10, IMAGES_LIMIT - current_count)
            if batch_size <= 0:
                break
            new_images = await fetch_images_from_wikipedia(category, batch_size, db)
            current_count = db.query(func.count(WikiImage.id)).scalar()
            await asyncio.sleep(1)

            
    except Exception as e:
        logger.error(f"Error in collector task: {str(e)}")
    finally:
        is_collector_running = False
        db.close()
        logger.info(f"Image collection complete. Current total: {current_count}")