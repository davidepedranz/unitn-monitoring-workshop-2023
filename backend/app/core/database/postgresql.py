import re
from asyncio import AbstractEventLoop
from typing import AsyncContextManager, Optional

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool


class PostgreSQL:
    """
    Handles the connection pool to the PostgreSQL database.
    """

    _UPDATE_ANSWER_REGEX = re.compile("^UPDATE (?P<n>[0-9]+)$")
    _DELETE_ANSWER_REGEX = re.compile("^DELETE (?P<n>[0-9]+)$")

    def __init__(
        self,
        connection_url: str,
        min_connections: int,
        max_connections: int,
        loop: Optional[AbstractEventLoop] = None,
    ):
        """
        Initialize the manager that handles connections to PostgreSQL.
        """
        self._connection_url: str = connection_url
        self._loop = loop
        self._min_connections = min_connections
        self._max_connections = max_connections
        self._pool: Optional[Pool] = None

    async def connect(self) -> None:
        """
        Initialize the connection pool.

        NOTE: it must be called only once during startup.
        """
        assert self._pool is None, "Connection pool already initialized"

        self._pool = await asyncpg.create_pool(
            dsn=self._connection_url,
            loop=self._loop,
            min_size=self._min_connections,
            max_size=self._max_connections,
        )

    async def disconnect(self) -> None:
        """
        Close the connection pool.

        NOTE: it must be called after initializing the connection pool, during shutdown.
        """
        assert self._pool is not None, "Connection pool was not initialized correctly"
        await self._pool.close()
        self._pool = None

    def acquire(self) -> AsyncContextManager[Connection]:
        """
        Acquire a connection from the connection pool.

        :return: a connection to PostgreSQL.
        """
        assert self._pool is not None, "Connection pool was not initialized correctly"
        return self._pool.acquire()  # type: ignore

    @classmethod
    def get_number_of_updated_rows(cls, raw_answer: str) -> int:
        """
        Parse the number of updated rows from a raw PostgreSQL response.
        """
        match = cls._UPDATE_ANSWER_REGEX.match(raw_answer)
        assert (
            match is not None
        ), f"{raw_answer} is not a valid response for an UPDATE statement"
        return int(match.group("n"))

    @classmethod
    def get_number_of_deleted_rows(cls, raw_answer: str) -> int:
        """
        Parse the number of delete rows from a raw PostgreSQL response.
        """
        match = cls._DELETE_ANSWER_REGEX.match(raw_answer)
        assert (
            match is not None
        ), f"{raw_answer} is not a valid response for a DELETE statement"
        return int(match.group("n"))
