from sqlalchemy import Boolean, Date, DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class RustPlusUser(Base):
    """A RustPlus user
    """
    __tablename__ = "rust_plus_users"

    steam_id = Column(Integer, primary_key=True)
    server_token_id = Column(String, ForeignKey("server_tokens.steam_id"))
    fcm_token = Column(String, nullable=True)
    
    server_token = relationship("ServerToken", back_populates="users")

class ServerToken(Base):
    __tablename__ ="server_tokens"
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
    
    users = relationship("RustPlusUser", back_populates="server_token")

class Player(Base):
    __tablename__ = "players"
    
    steam_id = Column(Integer, primary_key=True)

class Message(Base):
    """A Rust in-game message
    """
    __tablename__ = "messages"
    
    author_steam_id = Column(String, primary_key=True)
    author_name = Column(String, nullable=False)
    content = Column(String, nullable=True)
    timestamp = Column(Date)


# A rust plus device (smart switch, smart alarm, storage monitor)
class Device(Base):
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
