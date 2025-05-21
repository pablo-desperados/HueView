from datetime import datetime

from sqlalchemy import (JSON, Boolean, Column, DateTime, Float, Integer,
                        String, ARRAY, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/hueview"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class WikiImage(Base):
    __tablename__ = "wiki_images"
    
    id = Column(Integer, primary_key=True, index=True)
    source_page = Column(String, index=True)
    image_title = Column(String, index=True)
    image_url = Column(String, unique=True)
    category = Column(String, index=True)
    theme = Column(String, index=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    file_size = Column(Integer, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
    

    analyzed = Column(Boolean, default=False)
    dominant_colors = Column(JSON, nullable=True)
    avg_color = Column(JSON, nullable=True)  
    color_vector = Column(ARRAY(Float), nullable=True) 

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()