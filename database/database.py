from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import text
from .models import Base, Device
import os

DEBUG = True

class Database:
    def __init__(self):
        db_path = "sqlite:///database/db.db"
        engine = self.get_engine(db_path)

        # Check if the database file already exists
        if not os.path.exists(db_path):
            Base.metadata.create_all(engine)

        # Create the session factory
        
        self.session = scoped_session(sessionmaker(bind=engine))
        

    def get_session(self):
        return self.session

    def get_engine(self, db_path):
        engine = create_engine(db_path, echo=DEBUG)
        return engine

    ############

    def insert(self, table, data):
        match table:
            case 'device':
                self.insert_device(data)
            case _:
                print("DB ERROR - Unknown insertion table:", table)

    def insert_device(self, data):
        id = data['id']
        name = data['name']
        dev_type = data['dev_type']
        
        new_device = Device(id=id, name=name, dev_type=dev_type)
        
        session = self.session
        
        try:
            session.add(new_device)
            session.commit()
            dprint("Added device to DB")
        except Exception as e:
            session.rollback() # Probably violated PK uniqueness constraint. That's all G
            #dprint(f"Error adding user {id} to the database: {e}")
        finally:
            session.close()
        
        
        
        
    def query(self, what, table, where="1=1"):
        session = self.session
        
        try:
            result = session.execute(text(f"SELECT {what} FROM {table} WHERE {where}"))
            #print("RES", result.fetchall())
            rows = result.fetchall()
            return rows
        except Exception as e:
            session.rollback()
            print(f"Database error: {e}")
            return None
        finally:
            session.close()

@staticmethod
def dprint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)