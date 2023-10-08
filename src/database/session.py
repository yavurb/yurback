from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_engine(settings.database_uri)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)
