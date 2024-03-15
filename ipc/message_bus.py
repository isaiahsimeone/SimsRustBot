from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Dict, List
if TYPE_CHECKING:
    from ipc.bus_subscriber import BusSubscriber
    
import loguru
from log.log_config import get_colourised_name

from log.loggable import Loggable





import asyncio
from ipc.message import Message

class MessageBus(Loggable):
    """
    The MessageBus class acts as a central hub for message passing and event 
    subscription within an asynchronous application. It allows various components 
    of the system, referred to as subscribers, to publish messages to topics and 
    subscribe to receive messages from those topics.

    Subscribers can publish messages to any topic, and any subscriber subscribed 
    to that topic will receive the message asynchronously. The MessageBus keeps 
    track of the last message published under each topic, allowing new subscribers 
    or those who missed the last message to retrieve it.
    
    The :class:`logging_abc.Loggable` base class provides structured logging methods
    """
    def __init__(self) -> None:
        """Constructor method
        """
        # Map topics to a list of subscriber callback methods
        self.subscriptions: Dict[str, List[Callable]] = {}
        # The last message published under a topic
        self.last_message: Dict[str, Message] = {}
        self.info("I am ready")

    @loguru.logger.catch()
    async def publish(self, topic: str, message: Message, publisher: str) -> None:
        """Publish a message to the message BUS.

        :param topic: The topic this message falls under
        :type topic: str
        :param message: The message to publish to the bus, under the topic
        :type message: :class:`ipc.message.Message`
        :param publisher: The readable name of the publishing service
        :type publisher: str
        """
        self.debug(get_colourised_name(publisher), "published", repr(message), "under topic", topic)
        message.publisher = publisher
        
        self.last_message[topic] = message
        
        # Notify all subscribers about the message
        if topic in self.subscriptions:
            for callback in self.subscriptions[topic]:
                asyncio.create_task(callback(topic, message))
                
    @loguru.logger.catch()
    def subscribe(self, subscriber: BusSubscriber, topic: str) -> None:
        """Subscribe a bus subscriber to a topic

        :param subscriber: The subscriber
        :type subscriber: :class:`ipc.bus_subscriber.BusSubscriber`
        :param topic: The topic to subscribe to
        :type topic: str
        """
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.info(get_colourised_name(subscriber.__class__.__name__), "subscribed to", topic)
        self.subscriptions[topic].append(subscriber.on_message)

    @loguru.logger.catch()
    def unsubscribe(self, subscriber: BusSubscriber, topic: str) -> None:
        """Unsubscribe a bus subscriber from the specified topic

        :param subscriber: The subscriber
        :type subscriber: :class:`ipc.bus_subscriber.BusSubscriber`
        :param topic: The topic to unsubscribe from
        :type topic: str
        """
        if topic in self.subscriptions and subscriber.on_message in self.subscriptions[topic]:
            self.subscriptions[topic].remove(subscriber.on_message)
            if not self.subscriptions[topic]:
                del self.subscriptions[topic]
    
    @loguru.logger.catch()
    async def last_topic_message_or_wait(self, topic: str) -> Message:
        """Return the last message under the specified topic, or wait
        for the first message published under that topic (polls 
        asynchronously every 0.5 seconds)

        :param topic: The topic
        :type topic: str
        :return: The last message published under the specified topic
        :rtype: :class:`ipc.message.Message`
        """
        while topic not in self.last_message:
            await asyncio.sleep(0.5)
        return self.last_message[topic]
            
            
    @loguru.logger.catch
    def get_subscriber_topics(self, subscriber: BusSubscriber) -> List[str]:
        """Returns a list of the topics that the specified subscriber
        is subscribed to

        :param subscriber: The subscriber
        :type subscriber: :class:`ipc.bus_subscriber.BusSubscriber`
        :return: A list of the topics the subscriber is subscribed to
        :rtype: List[str]
        """
        subscribed_topics = []
        for topic, subscribers in self.subscriptions.items():
            if any(sub == subscriber.on_message for sub in subscribers):
                subscribed_topics.append(topic)
        return subscribed_topics
   
        
    