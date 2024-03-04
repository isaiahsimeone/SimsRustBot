from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    steam_id = Column(String, unique=True)
    discord_id = Column(String, unique=True)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    timestamp = Column(Integer)

    user = relationship("User", back_populates="messages")

# A rust plus device (smart switch, smart alarm, storage monitor)
class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dev_type = Column(Integer)
    

User.messages = relationship("Message", order_by=Message.id, back_populates="user")
