from abc import ABC, abstractmethod

import loguru
import asyncio
from ipc.message import Message
from ipc.message_bus import MessageBus
from log.loggable import Loggable

class BusSubscriber(ABC):
    def __init__(self, bus: MessageBus, subscriber_name: str = "UnknownSubscriber"):
        self.bus = bus
        self.subscriber_name = subscriber_name
        self.bus.subscribe(self, "global")
    
    @loguru.logger.catch()
    async def subscribe(self, topic: str):
        """Subscribe to a topic

        :param topic: The topic to subscribe to
        :type topic: str
        """
        self.bus.subscribe(self, topic)

    @loguru.logger.catch()
    async def unsubscribe(self, topic: str):
        """Unsubscribe from a topic

        :param topic: The topic to unsubscribe from
        :type topic: str
        """
        self.bus.unsubscribe(self, topic)

    @loguru.logger.catch()
    async def publish(self, topic: str, message: Message):
        """Publish a message to the bus

        :param topic: The topic to publish this message under
        :type topic: str
        :param message: The message to publish to the bus
        :type message: :class:`ipc.message.Message`
        """
        return await self.bus.publish(topic, message, self.subscriber_name)

    @loguru.logger.catch()
    @abstractmethod
    async def on_message(self, topic: str, message: Message):
        """Handle a bus message pertaining to a subscribed topic

        :param topic: The topic this bus message falls under
        :type topic: str
        :param message: The message from the bus
        :type message: :class:`ipc.message.Message`
        """
        pass
    
    @loguru.logger.catch()
    async def last_topic_message_or_wait(self, topic: str):
        return await self.bus.last_topic_message_or_wait(topic)
    
    @loguru.logger.catch()
    @abstractmethod
    async def execute(self):
        """The point of execution for the BusSubscriber class
        """
        pass