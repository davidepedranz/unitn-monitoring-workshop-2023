from typing import Optional, Tuple
from uuid import UUID

from app.core.database.repository.base import Repository
from app.core.todo import Todo


# TODO: measure the execution time of the different database operations
class InstrumentedRepository(Repository):
    """
    Prometheus-instrumented decorator for a concrete implementation of Repository.
    Please use it as follows:
    ```
        basic_repository = ...
        instrumented_repository = InstrumentedRepository(basic_repository)
    ```
    """

    def __init__(self, repository: Repository):
        self._repository = repository

    async def init(self) -> None:
        await self._repository.init()

    async def get(self, id_: UUID) -> Optional[Todo]:
        return await self._repository.get(id_=id_)

    async def list(self) -> Tuple[Todo, ...]:
        return await self._repository.list()

    async def insert(self, text: str) -> UUID:
        return await self._repository.insert(text=text)

    async def edit_text(self, id_: UUID, text: str) -> bool:
        return await self._repository.edit_text(id_=id_, text=text)

    async def activate(self, id_: UUID) -> bool:
        return await self._repository.activate(id_=id_)

    async def deactivate(self, id_: UUID) -> bool:
        return await self._repository.deactivate(id_=id_)

    async def delete(self, id_: UUID) -> bool:
        return await self._repository.delete(id_=id_)
