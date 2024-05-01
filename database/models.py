from sqlalchemy import Boolean, Date, DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class DBRustPlusUser(Base):
    __tablename__ = "rust_plus_users"
    
    steam_id = Column(Integer, primary_key=True)
    server_token_id = Column(String, ForeignKey("server_tokens.steam_id"))
    server_token = relationship("DBServerToken", back_populates="users")

class DBServerToken(Base):
    __tablename__ = "server_tokens"
    steam_id = Column(String, primary_key=True)
    desc = Column(String, nullable=True)
    id = Column(String, nullable=False)
    img = Column(String, nullable=True)
    ip = Column(String, nullable=False)
    logo = Column(String, nullable=True)
    name = Column(String, nullable=False)
    playerToken = Column(String, nullable=False)
    port = Column(String, nullable=False)
    type_ = Column(String, nullable=True)
    url = Column(String, nullable=True)
    
    users = relationship("DBRustPlusUser", back_populates="server_token")

class DBEncounteredFCMMessage(Base):
    __tablename__ = "encountered_fcm_messages"
    
    message_id = Column(String, primary_key=True)

class DBPlayer(Base):
    __tablename__ = "players"
    
    steam_id = Column(Integer, primary_key=True)

class DBMessage(Base):
    """A Rust in-game message
    """
    __tablename__ = "messages"
    
    author_steam_id = Column(String, primary_key=True)
    author_name = Column(String, nullable=False)
    content = Column(String, nullable=True)
    timestamp = Column(Date)


# A rust plus device (smart switch, smart alarm, storage monitor)
class DBDevice(Base):
    """A Rust device
    """
    __tablename__ = "devices"
    
    entity_id = Column(Integer, primary_key=True)
    name = Column(String)
    device_type = Column(Integer)
    state = Column(Boolean) # For smart switches - true == on



# Setup the database engine and session factory (to be imported in DatabaseService)
def db_setup(database_url: str):
    engine = create_engine("sqlite:///" + database_url, echo=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
