import asyncio
from typing import NamedTuple

from app.config import Config
from app.core.database import (
    InstrumentedRepository,
    PostgreSQL,
    PostgreSQLRepository,
    Repository,
)


class Dependencies(NamedTuple):
    postgresql: PostgreSQL
    repository: Repository

    async def init(self) -> None:
        await asyncio.gather(
            self.postgresql.connect(),
        )
        await self.repository.init()

    async def shutdown(self, timeout_seconds: float) -> None:
        await asyncio.wait_for(
            asyncio.gather(
                self.postgresql.disconnect(),
            ),
            timeout=timeout_seconds,
        )


def setup_dependencies(config: Config) -> Dependencies:
    postgresql = PostgreSQL(
        connection_url=config.postgresql_connection_url.get_secret_value(),
        min_connections=config.postgresql_min_connections,
        max_connections=config.postgresql_max_connections,
    )

    repository = PostgreSQLRepository(postgresql=postgresql)
    instrumented_repository = InstrumentedRepository(repository)

    return Dependencies(postgresql=postgresql, repository=instrumented_repository)
