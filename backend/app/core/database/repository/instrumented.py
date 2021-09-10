from typing import Optional, Tuple
from uuid import UUID

from prometheus_client import Histogram

from app.core.database.repository.base import Repository
from app.core.todo import Todo


# TASK: measure the execution time of the different database operations
# SOLUTION: we create a new `Histogram` object and wrap each call with the `.time()` context
#           manager to measure the execution time; we use a label to identify the operation
class InstrumentedRepository(Repository):
    """
    Prometheus-instrumented decorator for a concrete implementation of Repository.
    Please use it as follows:
    ```
        basic_repository = ...
        instrumented_repository = InstrumentedRepository(basic_repository)
    ```
    """

    _HISTOGRAM = Histogram(
        name="app_query_duration",
        unit="seconds",
        documentation="Time required to handle a query to the Todos repository",
        labelnames=("query",),
    )

    def __init__(self, repository: Repository):
        self._repository = repository

    async def init(self) -> None:
        with self._HISTOGRAM.labels(query="init").time():
            await self._repository.init()

    async def get(self, id_: UUID) -> Optional[Todo]:
        with self._HISTOGRAM.labels(query="get").time():
            return await self._repository.get(id_=id_)

    async def list(self) -> Tuple[Todo, ...]:
        with self._HISTOGRAM.labels(query="list").time():
            return await self._repository.list()

    async def insert(self, text: str) -> UUID:
        with self._HISTOGRAM.labels(query="insert").time():
            return await self._repository.insert(text=text)

    async def edit_text(self, id_: UUID, text: str) -> bool:
        with self._HISTOGRAM.labels(query="edit_text").time():
            return await self._repository.edit_text(id_=id_, text=text)

    async def activate(self, id_: UUID) -> bool:
        with self._HISTOGRAM.labels(query="activate").time():
            return await self._repository.activate(id_=id_)

    async def deactivate(self, id_: UUID) -> bool:
        with self._HISTOGRAM.labels(query="deactivate").time():
            return await self._repository.deactivate(id_=id_)

    async def delete(self, id_: UUID) -> bool:
        with self._HISTOGRAM.labels(query="delete").time():
            return await self._repository.delete(id_=id_)
