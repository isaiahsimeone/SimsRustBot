from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
import os


def init_db(config):
    db_path = config.get("database").get("path")

    # Check if the database file already exists
    if not os.path.exists(db_path):
        Base.metadata.create_all(engine)
        
    engine = get_engine(db_path)

        
def get_engine(db_path):
    engine = create_engine(db_path, echo=True)
    return engine

# Session factory, bound to the engine
Session = sessionmaker(bind=get_engine())
