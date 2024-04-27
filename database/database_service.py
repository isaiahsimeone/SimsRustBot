
from __future__ import annotations
import asyncio
import json
from typing import TYPE_CHECKING, List

import loguru

from database.models import RustPlusUser, ServerToken, db_setup
from ipc.data_models import PlayerServerToken, DatabasePlayerServerTokens
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
        
        # Get config
        self.config = (await self.last_topic_message_or_wait("config")).data["config"]
        
        database_filepath = self.config["DatabaseService"]["path"] # gives a path to a .db
        
        # Initialise the database
        self.session = db_setup(database_filepath)
        
        # Fetch stored player tokens, and publish
        # publish under database_player_server_tokens
        server_tokens = [PlayerServerToken.from_database_server_token(t) for t in self.get_all_server_tokens()]
        await self.publish("database_player_server_tokens", DatabasePlayerServerTokens(tokens=server_tokens))
        
        # Get socket
        await self.last_topic_message_or_wait("socket_ready")
        self.socket = await RustSocketManager.get_instance()
        
        await asyncio.Future()
        
    
    def upsert_server_token(self, session: Session, token_data: dict):
        try:
            user = session.query(RustPlusUser).filter_by(steam_id=token_data['steam_id']).one_or_none()
            if user is None:
                user = RustPlusUser(steam_id=token_data['steam_id'])
                session.add(user)
            
            token = session.query(ServerToken).filter_by(steam_id=token_data['steam_id']).one_or_none()
            if token is None:
                token = ServerToken(steam_id=token_data['steam_id'])
                session.add(token)
            
            # Ensure that `ServerToken` is linked correctly
            user.server_token_id = token.steam_id

            # Populate `ServerToken` fields
            token.desc = token_data.get('desc', '')
            token.id = token_data['id']
            token.img = token_data.get('img', '')
            token.ip = token_data['ip']
            token.logo = token_data.get('logo', '')
            token.name = token_data['name']
            token.playerToken = token_data['playerToken']
            token.port = token_data['port']
            token.type_ = token_data.get('type_', '')
            token.url = token_data.get('url', '')

            session.commit()
        except Exception as e:
            session.rollback()
            self.error(f"Database error: {e}")

            
    def get_all_server_tokens(self):
        session = self.session()
        try:
            tokens = session.query(ServerToken).all()
            return tokens
        except Exception as e:
            self.error(f"Failed to fetch server tokens: {e}")
            return []
        finally:
            session.close()
    
    @loguru.logger.catch
    async def on_message(self, topic: str, message: Message):
        self.info("GOT A MESSAGE topic:", topic)
        match topic:
            case "player_server_token":
                token = message.data
                
                self.upsert_server_token(self.session(), token)

                
            case "player_fcm_token":
                pass
            case _:
                self.error("Received a message that I don't have a case for")