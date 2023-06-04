from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import db_config

engine = create_engine(db_config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
