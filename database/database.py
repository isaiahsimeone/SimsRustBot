from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os

def init_db(config):
    db_path = config.get("database", {}).get("path", "sqlite:///database/db.db")
    engine = get_engine(db_path)

    # Check if the database file already exists
    if not os.path.exists(db_path):
        Base.metadata.create_all(engine)

    # Create the session factory
    global Session
    Session = sessionmaker(bind=engine)

def get_engine(db_path):
    engine = create_engine(db_path, echo=True)
    return engine
