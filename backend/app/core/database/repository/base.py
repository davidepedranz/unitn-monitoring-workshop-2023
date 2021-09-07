from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from app.core.todo import Todo


class Repository(ABC):
    """
    Repository for Todos: define methods to retrieve, insert, modify and delete Todos.
    """

    @abstractmethod
    async def init(self) -> None:
        """
        Initialize the database schema.
        """

    @abstractmethod
    async def get(self, id_: UUID) -> Optional[Todo]:
        """
        Retrieve a Todo by its ID.
        """

    @abstractmethod
    async def list(self) -> tuple[Todo, ...]:
        """
        Retrieve all stored Todos.
        """

    @abstractmethod
    async def insert(self, text: str) -> UUID:
        """
        Insert a new active Todo.
        """

    @abstractmethod
    async def edit_text(self, id_: UUID, text: str) -> bool:
        """
        Edit the text for an existing Todo.
        """

    @abstractmethod
    async def activate(self, id_: UUID) -> bool:
        """
        Mark an existing Todo as active.

        :param id_: ID of the Todo to update.
        :return: True if the Todo was found and correctly updated, false otherwise.
        """

    @abstractmethod
    async def deactivate(self, id_: UUID) -> bool:
        """
        Mark an existing Todo as not active.

        :param id_: ID of the Todo to update.
        :return: True if the Todo was found and correctly updated, false otherwise.
        """

    @abstractmethod
    async def delete(self, id_: UUID) -> bool:
        """
        Delete an existing Todo.

        :param id_: ID of the Todo to delete.
        :return: True if the Todo was found and correctly deleted, false otherwise.
        """
