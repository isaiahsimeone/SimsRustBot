"""The MessageBus class facilitates decoupled interactions among
different components of the system, enabling them to publish
and subscribe to messages associated with specific topics.

The MessageBus class allows components, referred to as subscribers, to communicate with
each other without direct references. Subscribers can publish messages to any topic, and
all subscribers to that topic receive the messages asynchronously. This mechanism supports
a publish-subscribe pattern, enhancing modularity and separation of concerns within the
application.

Key Features:
------------

- **Publish-Subscribe Mechanism**: Components can publish messages to topics and subscribe
  to receive messages from those topics, enabling asynchronous, decoupled communication.
- **Last Message Tracking**: The MessageBus keeps track of the last message published under
  each topic, allowing subscribers to access recent messages even if they missed the
  publication event.
- **Asynchronous Operation**: The class is designed to work in an asynchronous environment,
  leveraging asyncio for non-blocking operation and efficient handling of concurrent
  message publication and subscription.
- **Structured Logging**: Inherits from :class:`log.loggable.Loggable`, providing structured and configurable
  logging capabilities to facilitate debugging and monitoring of message bus activities.

Usage:
-----

The MessageBus class is intended to be used as a singleton within an application, ensuring
a single, shared instance manages all message passing and subscriptions. Components wishing
to communicate via the message bus must first subscribe to the topics of interest and can
then publish messages to those topics as needed.

Example:
-------
.. code-block:: python

    from message_bus import MessageBus

    # Initialise the message bus
    bus = MessageBus()

    # Define a subscriber callback function
    async def on_message_received(topic: str, message: Message):
        print(f"Received message on topic {topic}: {message}")

    # Subscribe to a topic
    bus.subscribe(subscriber=on_message_received, topic="example_topic")

    # Publish a message to the topic
    await bus.publish(topic="example_topic", message="Hello, World!", publisher="ExamplePublisher")

"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ipc.bus_subscriber import BusSubscriber
    from ipc.message import Message

import asyncio

import loguru

from log.log_config import get_colourised_name
from log.loggable import Loggable


class MessageBus(Loggable):
    """The MessageBus class acts as a central hub for message passing and event
    subscription within the bot. It allows various components of the
    system, referred to as subscribers, to publish messages to topics and
    subscribe to receive messages from those topics.
    |
    Subscribers can publish messages to any topic, and any subscriber subscribed
    to that topic will receive the message asynchronously. The MessageBus keeps
    track of the last message published under each topic, allowing new subscribers
    or those who missed the last message to retrieve it.
    """

    def __init__(self: MessageBus) -> None:
        """Constructor method.
        """
        # Map topics to a list of subscriber callback methods
        self.subscriptions: dict[str, list[Callable]] = {}
        # The last message published under a topic
        self.last_message: dict[str, Message] = {}
        # Set of background tasks
        self.background_tasks: set[asyncio.Task] = set()

        self.info("MessageBus initialised")

    @loguru.logger.catch()
    async def publish(self: MessageBus, topic: str, message: Message, publisher: str, wait_for_reply: bool = False) -> None:
        """Publish a message to the message BUS.

        :param topic: The topic this message falls under
        :type topic: str
        :param message: The message to publish to the bus, under the topic
        :type message: :class:`Message <ipc.message.Message>`
        :param publisher: The readable name of the publishing service
        :type publisher: str
        :param wait_for_reply: True if the caller should block until a reply to this message is received, False otherwise
        :type wait_for_reply: bool
        """
        self.debug(get_colourised_name(publisher), "published", repr(message), "under topic", topic)
        message.publisher = publisher

        self.last_message[topic] = message
        
        # TODO: check here if someone is waiting on this message, then call them back with it

        # Notify all subscribers of the message
        if topic in self.subscriptions:
            for callback in self.subscriptions[topic]:
                task = asyncio.create_task(callback(topic, message))
                self.background_tasks.add(task)

    @loguru.logger.catch()
    def subscribe(self: MessageBus, subscriber: BusSubscriber, topic: str) -> None:
        """Subscribe a bus subscriber to a topic.

        :param subscriber: The subscriber
        :type subscriber: :class:`BusSubscriber <ipc.bus_subscriber.BusSubscriber>`
        :param topic: The topic to subscribe to
        :type topic: str
        """
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        self.info(get_colourised_name(subscriber.__class__.__name__), f"subscribed to topic '{topic}'")
        self.subscriptions[topic].append(subscriber.on_message)

    @loguru.logger.catch()
    def unsubscribe(self: MessageBus, subscriber: BusSubscriber, topic: str) -> None:
        """Unsubscribe a bus subscriber from the specified topic.

        :param subscriber: The subscriber
        :type subscriber: :class:`BusSubscriber <ipc.bus_subscriber.BusSubscriber>`
        :param topic: The topic to unsubscribe from
        :type topic: str
        """
        if topic in self.subscriptions and subscriber.on_message in self.subscriptions[topic]:
            self.subscriptions[topic].remove(subscriber.on_message)
            if not self.subscriptions[topic]:
                del self.subscriptions[topic]

    @loguru.logger.catch()
    async def last_topic_message_or_wait(self: MessageBus, topic: str) -> Message:
        """Return the last message under the specified topic, or wait
        for the first message published under that topic (polls
        asynchronously every 0.5 seconds).

        :param topic: The topic
        :type topic: str
        :return: The last message published under the specified topic
        :rtype: :class:`Message <ipc.message.Message>`
        """
        while topic not in self.last_message:
            await asyncio.sleep(0.5)
        return self.last_message[topic]

    @loguru.logger.catch
    def get_subscriber_topics(self: MessageBus, subscriber: BusSubscriber) -> list[str]:
        """Returns a list of the topics that the specified subscriber
        is subscribed to.

        :param subscriber: The subscriber
        :type subscriber: :class:`BusSubscriber <ipc.bus_subscriber.BusSubscriber>`
        :return: A list of the topics the subscriber is subscribed to
        :rtype: List[str]
        """
        subscribed_topics = []
        for topic, subscribers in self.subscriptions.items():
            if any(sub == subscriber.on_message for sub in subscribers):
                subscribed_topics.append(topic)
        return subscribed_topics
