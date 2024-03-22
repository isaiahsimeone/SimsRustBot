from abc import ABC, abstractmethod

import loguru

from ipc.data_models import BaseModel
from ipc.message import Message
from ipc.message_bus import MessageBus


class BusSubscriber(ABC):
    def __init__(self: "BusSubscriber", bus: MessageBus, subscriber_name: str = "UnknownSubscriber") -> None:
        self.bus = bus
        self.subscriber_name = subscriber_name
        self.bus.subscribe(self, "global")

    @loguru.logger.catch()
    async def subscribe(self: "BusSubscriber", topic: str) -> None:
        """Subscribe to a topic.

        :param topic: The topic to subscribe to
        :type topic: str
        """
        self.bus.subscribe(self, topic)

    @loguru.logger.catch()
    async def unsubscribe(self: "BusSubscriber", topic: str) -> None:
        """Unsubscribe from a topic.

        :param topic: The topic to unsubscribe from
        :type topic: str
        """
        self.bus.unsubscribe(self, topic)

    @loguru.logger.catch()
    async def publish(self: "BusSubscriber", topic: str, message: BaseModel, wait_for_reply: bool = False) -> None:
        """Publish a message to the bus.

        :param topic: The topic to publish this message under
        :type topic: str
        :param message: The message to publish to the bus
        :type message: :class:`Message <ipc.message.Message>`
        :param wait_for_reply: True if the caller should block until a reply to this message is received, False otherwise
        :type wait_for_reply: bool
        """
        return await self.bus.publish(topic, Message(message), self.subscriber_name, wait_for_reply)

    @loguru.logger.catch()
    @abstractmethod
    async def on_message(self: "BusSubscriber", topic: str, message: Message) -> None:
        """Handle a bus message pertaining to a subscribed topic.

        :param topic: The topic this bus message falls under
        :type topic: str
        :param message: The message from the bus
        :type message: :class:`Message <ipc.message.Message>`
        """

    @loguru.logger.catch()
    async def last_topic_message_or_wait(self: "BusSubscriber", topic: str) -> Message:
        """Get the last message published under a topic, or wait
        for the first message published under that topic.

        :param topic: The topic
        :type topic: str
        :return: The last message under the topic
        :rtype: :class:`Message <ipc.message.Message>`
        """
        return await self.bus.last_topic_message_or_wait(topic)

    @loguru.logger.catch()
    def last_topic_message(self: "BusSubscriber", topic: str) -> Message | None:
        return self.bus.last_topic_message(topic)

    @loguru.logger.catch()
    @abstractmethod
    async def execute(self: "BusSubscriber") -> None:
        """The point of execution for the BusSubscriber class.
        """
