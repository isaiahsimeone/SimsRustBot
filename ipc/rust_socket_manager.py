"""RustSocketManager is responsible for managing connections to the Rust
game server using the RustSocket interface. It implements a singleton pattern to
ensure that only one instance of RustSocket is created and utilised throughout an application.

The RustSocketManager is responsible for initialising the connection to the Rust server with
specific server details (IP address, port, playerId, and playerToken) and provides a mechanism
for retrieving the RustSocket instance for performing operations on the server.

Usage:
-----

Before using the RustSocketManager to interact with a Rust server, the singleton instance
must be initialised and the RustSocket configured with the server's connection details.

First, ensure the RustSocketManager is initialised:

.. code-block:: python

    RustSocketManager.initialise()

Then, retrieve the instance and initialise the RustSocket with the server details:

.. code-block:: python

    manager = asyncio.run(RustSocketManager.get_instance())

    await manager.initialise_socket(ip="<server_ip>", port="<server_port>",
        playerId="<steamId>", playerToken="<playerToken>")

With the RustSocket initialised, you can now access it via the `socket` property
of the RustSocketManager instance to perform various operations on the Rust server.

Key Features:
------------

- Implements the singleton design pattern for managing the RustSocket instance.
- Provides thread-safe and asynchronous retrieval of the RustSocketManager instance.
- Ensures that only one connection to the Rust server is established and reused.

"""
from __future__ import annotations

import asyncio

from rustplus import RustSocket
from rustplus.exceptions.exceptions import ServerNotResponsiveError

from log.loggable import Loggable


class RustSocketManager(Loggable):
    """A manager class for handling the lifecycle and operations of a RustSocket instance.

    This class uses the singleton pattern to ensure only one instance of RustSocket is created
    and shared across the program.

    """

    instance = None
    lock = asyncio.Lock()

    def __init__(self: RustSocketManager) -> None:
        """Initialises a RustSocketManager instance.
        """
        self.rust_socket = None

    @classmethod
    def initialise(cls: type[RustSocketManager]) -> None:
        """Initialises the singleton instance of RustSocketManager if it hasn't been initialised already.

        This method should be called before any retrievals of the RustSocketManager
        instance are performed.
        """
        if cls.instance is None:
            cls.instance = cls()
        else:
            cls.instance.warning("RustSocketManager is already initialised.")

    @classmethod
    async def get_instance(cls: type[RustSocketManager]) -> RustSocketManager:
        """Asynchronously retrieves the singleton instance of RustSocketManager
        If the instance has not been initialised yet, it initialises the singleton instance.

        :return: The singleton instance of the :class:`RustSocketManager <ipc.rust_socket_manager.RustSocketManager>`
        :rtype: Self
        """
        async with cls.lock:
            if cls.instance is None:
                cls.instance = cls()
            return cls.instance

    async def initialise_socket(self: RustSocketManager, ip: str, port: str, playerId: str, playerToken: str) -> None:
        """Initialise the rust socket.

        connect to a rust server with the provided
        details. If unable to connect to a server with these details, a critical error
        is raised, and the program will exit.

        :param ip: The IP address of the rust server
        :type ip: str
        :param port: The port of the rust server
        :type port: str
        :param playerId: The playerId of the person running the bot (steamId)
        :type playerId: str
        :param playerToken: The playerToken of the person running the bot
        :type playerToken: str
        :return: Nothing
        :rtype: None
        """
        if not self.rust_socket:
            try:
                self.rust_socket = RustSocket(ip, port, int(playerId), int(playerToken))
                await self.rust_socket.connect()
            except ServerNotResponsiveError:
                self.critical(f"Unable to connect to server {ip}:{port}. Server is unresponsive")

    @property
    def socket(self: RustSocketManager) -> RustSocket:
        """Access the rust socket. The socket should be initialised
        with :meth:`initialise_socket` before access.

        If an attempt to access the socket before initialisation is
        made, a critical error is raised, which will terminate the program

        :return: The rust socket
        :rtype: :class:`RustSocket`
        """
        if not self.rust_socket:
            self.critical("Tried to fetch socket before initialisation")
        return self.rust_socket
