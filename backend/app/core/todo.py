from uuid import UUID

from pydantic import BaseModel


class Todo(BaseModel):
    class Config:
        frozen = True

    id: UUID
    text: str
    active: bool
