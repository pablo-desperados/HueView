import asyncio
import logging
from contextlib import asynccontextmanager

from collector import collect_images_task, is_collector_running
from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import create_tables
from routes import router

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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





@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    logger.info("Starting application and background tasks")
    task = asyncio.create_task(collect_images_task())
    
    yield
    
    import collector
    collector.is_collector_running = False
    
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        logger.info("Scraper has been cancelled")
    
    
    
    
    
app = FastAPI(title="HueView",lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    