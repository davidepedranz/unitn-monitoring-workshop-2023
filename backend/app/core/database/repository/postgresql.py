from typing import Optional
from uuid import UUID

from app.core.database.postgresql import PostgreSQL
from app.core.database.repository.base import Repository
from app.core.delay import random_delay, rare_delay
from app.core.todo import Todo


class PostgreSQLRepository(Repository):
    """
    PostgreSQL based implementation of a Todos repository.
    """

    class SQL:
        CREATE_UUID_EXTENSION = """
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """

        CREATE_TABLE = """
            CREATE TABLE IF NOT EXISTS todos
            (
                id     uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
                text   text NOT NULL,
                active bool NOT NULL
            );
        """

        GET = """
            SELECT *
            FROM todos
            WHERE id = $1
        """

        LIST = """
            SELECT id, text, active
            FROM todos
            ORDER BY id;
        """

        INSERT = """
            INSERT INTO todos(text, active)
            VALUES ($1, $2)
            RETURNING id;
        """

        EDIT_TEXT = """
            UPDATE todos
            SET text = $1
            WHERE id = $2;
        """

        ACTIVATE = """
            UPDATE todos
            SET active = TRUE
            WHERE id = $1;
        """

        DEACTIVATE = """
            UPDATE todos
            SET active = FALSE
            WHERE id = $1;
        """

        DELETE = """
            DELETE FROM todos
            WHERE id = $1;
        """

    def __init__(self, postgresql: PostgreSQL):
        self._postgresql = postgresql

    async def init(self) -> None:
        async with self._postgresql.acquire() as connection:
            await connection.execute(self.SQL.CREATE_UUID_EXTENSION)
            await connection.execute(self.SQL.CREATE_TABLE)

    async def get(self, id_: UUID) -> Optional[Todo]:
        async with self._postgresql.acquire() as connection:
            row = await connection.fetchrow(self.SQL.GET, id_)

            if row is None:
                return None

            return Todo.model_validate(dict(row))

    async def list(self) -> tuple[Todo, ...]:
        async with self._postgresql.acquire() as connection:
            rows = await connection.fetch(self.SQL.LIST)
            return tuple(Todo.model_validate(dict(row)) for row in rows)

    async def insert(self, text: str) -> UUID:
        async with self._postgresql.acquire() as connection:
            raw = await connection.fetchval(self.SQL.INSERT, text, True)
            return UUID(str(raw))

    async def edit_text(self, id_: UUID, text: str) -> bool:
        async with self._postgresql.acquire() as connection:
            raw_answer = await connection.execute(self.SQL.EDIT_TEXT, text, id_)
            return PostgreSQL.get_number_of_updated_rows(raw_answer) > 0

    async def activate(self, id_: UUID) -> bool:
        async with self._postgresql.acquire() as connection:
            raw_answer = await connection.execute(self.SQL.ACTIVATE, id_)
            return PostgreSQL.get_number_of_updated_rows(raw_answer) > 0

    async def deactivate(self, id_: UUID) -> bool:
        async with self._postgresql.acquire() as connection:
            raw_answer = await connection.execute(self.SQL.DEACTIVATE, id_)
            return PostgreSQL.get_number_of_updated_rows(raw_answer) > 0

    async def delete(self, id_: UUID) -> bool:
        async with self._postgresql.acquire() as connection:
            raw_answer = await connection.execute(self.SQL.DELETE, id_)
            return PostgreSQL.get_number_of_deleted_rows(raw_answer) > 0
