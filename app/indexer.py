import os
import tempfile
import numpy as np
import httpx
from PIL import Image
import io
import logging
from typing import List, Tuple, Dict, Any
from sklearn.cluster import KMeans
from scipy.spatial import KDTree
import pickle
from sqlalchemy import func
from concurrent.futures import ThreadPoolExecutor

from models import WikiImage, SessionLocal


# CONSTANTS FOR INDEXING

DOMINANT_CNT =5
INDEX_PATH = "image_kdtree.pickle" 
TEMP_DIR = "temp_images" 

logger = logging.getLogger(__name__)
os.makedirs(TEMP_DIR, exist_ok=True)

class ImageIndexer:
    def __init__(self) -> None:
        self.tree = None
        self.image = []
    
    async def download_image_temp(self, image_url: str) -> str:
        try:
            fd, temp_path = tempfile.mkstemp(dir=TEMP_DIR, suffix=".jpg")
            os.close(fd)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                
                if response.status_code == 200:
                    with open(temp_path, 'wb') as f:
                        f.write(response.content)
                    return temp_path
                else:
                    logger.error(f"Failed to download image: {response.status_code}")
                    return None
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return None
        
    async def build_index(self, force_rebuild=False):
        db = SessionLocal()
        try:
            logger.info("INIT INDEXER")
        except Exception as e:
            logger.error(f"Error building index: {str(e)}")
        finally:
            db.close()
            
indexer = ImageIndexer()
