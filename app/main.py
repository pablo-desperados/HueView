from fastapi import FastAPI, BackgroundTasks
import httpx
import asyncio
import os
import json
from typing import List, Dict, Optional
import random
import logging
from fastapi.middleware.cors import CORSMiddleware
from routes import routes

app = FastAPI(title="HueView")


IMAGES_LIMIT = 1000
images_collected = 0
is_collector_running = False
image_data = []

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)