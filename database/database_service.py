
from __future__ import annotations
import asyncio
import json
from typing import TYPE_CHECKING, List

import loguru

from database.models import DBEncounteredFCMMessage, DBRustPlusUser, DBServerToken, db_setup
from ipc.data_models import DatabaseEncounteredFCMMessages, FCMMessage, PlayerServerToken, DatabasePlayerServerTokens
from rust_socket.rust_socket_manager import RustSocketManager
if TYPE_CHECKING:
    pass
from sqlalchemy.sql import text
from ipc.bus_subscriber import BusSubscriber
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

from sqlalchemy.orm import Session

from rustplus import RustSocket

class DatabaseService(BusSubscriber, Loggable):
    def __init__(self, bus: MessageBus):
        super().__init__(bus, self.__class__.__name__)
        self.socket: RustSocketManager
        self.bus = bus
        self.config = {}

    @loguru.logger.catch
    async def execute(self):
        await self.subscribe("player_server_token")
        await self.subscribe("player_fcm_token")
        await self.subscribe("fcm_message")
        
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        
        database_filepath = self.config["DatabaseService"]["path"] # gives a path to a .db
        
        # Initialise the database
        self.session = db_setup(database_filepath)
        
        # Fetch stored player tokens, and publish
        # publish under database_player_server_tokens
        server_tokens = [PlayerServerToken.from_database_entry(t) for t in self.get_all_server_tokens()]
        await self.publish("database_player_server_tokens", DatabasePlayerServerTokens(tokens=server_tokens))
        
        # Publish the list of FCM messages that have been encountered
        encountered_messages = self.get_encountered_fcm_messages_set()
        await self.publish("database_encountered_fcm_messages", DatabaseEncounteredFCMMessages(encountered_messages=encountered_messages))
        
        # Get socket
        await self.last_topic_message_or_wait("socket_ready")
        self.socket = await RustSocketManager.get_instance()
        
        await asyncio.Future()
        
    
    def upsert_server_token(self, token_data: dict):
        session = self.session()
        try:
            user = session.query(DBRustPlusUser).filter_by(steam_id=token_data["steam_id"]).one_or_none()
            if user is None:
                user = DBRustPlusUser(steam_id=token_data["steam_id"])
                session.add(user)
            
            token = session.query(DBServerToken).filter_by(steam_id=token_data["steam_id"]).one_or_none()
            if token is None:
                token = DBServerToken(steam_id=token_data["steam_id"])
                session.add(token)
            
            # Ensure that `ServerToken` is linked correctly
            user.server_token_id = token.steam_id

            # Populate ServerToken fields
            token.desc = token_data["desc"]
            token.id = token_data["id"]
            token.img = token_data["img"]
            token.ip = token_data["ip"]
            token.logo = token_data["logo"]
            token.name = token_data["name"]
            token.playerToken = token_data["playerToken"]
            token.port = token_data["port"]
            token.type_ = token_data.get("type_", "")
            token.url = token_data.get("url", "")

            session.commit()
        except Exception as e:
            session.rollback()
            self.error(f"Database error: {e}")
        finally:
            session.close()

            
    def get_all_server_tokens(self):
        session = self.session()
        try:
            tokens = session.query(DBServerToken).all()
            return tokens
        except Exception as e:
            self.error(f"Failed to fetch server tokens: {e}")
            return []
        finally:
            session.close()
            
    def get_encountered_fcm_messages_set(self):
        session = self.session()
        try:
            message_ids = session.query(DBEncounteredFCMMessage.message_id).all()
            encountered_message_ids = {id[0] for id in message_ids}  # id[0] because `all()` returns a list of tuples
            return encountered_message_ids
        except Exception as e:
            self.error(f"Failed to fetch encountered FCM messages: {e}")
            return set()  # Return an empty set on failure
        finally:
            session.close()


    
    def insert_fcm_message(self, fcm_message: dict) -> None:
        session = self.session()
        try:
            # Is this device in the table already? If it is, just return
            fcm_message_id = fcm_message["fcm_message_id"]
            encountered_message = session.query(DBEncounteredFCMMessage).filter_by(message_id=fcm_message_id).one_or_none()

            if encountered_message is not None:
                self.warning(f"FCM Message has already been encountered ({encountered_message.message_id}). No insertion needed")
                session.close()
                return None
            
            # Hasn't been encountered, mark it as encountered by insert it
            encountered_message = DBEncounteredFCMMessage(message_id=fcm_message["fcm_message_id"])

            session.add(encountered_message)
            session.commit()
        except Exception as e:
            session.rollback()
            self.error(f"Database error: {e}")
        finally:
            session.close()
    
    @loguru.logger.catch
    async def on_message(self, topic: str, message: Message):
        self.info("GOT A MESSAGE topic:", topic)
        match topic:
            case "player_server_token":
                self.upsert_server_token(message.data) # inserting data_models.PlayerServerToken
            case "player_fcm_token":
                pass
            case "fcm_message":
                self.insert_fcm_message(message.data) # inserting data_models.FCMMessage
            case _:
                self.error("Received a message that I don't have a case for")