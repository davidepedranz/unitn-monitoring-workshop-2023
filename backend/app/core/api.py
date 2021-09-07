from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, Path, Response, status

from app.core.database import Repository
from app.core.todo import Todo


def create_todos_router(repository: Repository) -> APIRouter:
    """
    Create a FastAPI router that contains the endpoint for all Todo REST APIs.
    """
    router = APIRouter(prefix="/todos")

    @router.get("/{id}")
    async def get_todo(id_: UUID = Path(..., alias="id")) -> Todo:
        todo = await repository.get(id_)
        if todo is None:
            raise HTTPException(status_code=404, detail="Item not found")
        else:
            return todo

    @router.get("/")
    async def list_todos() -> tuple[Todo, ...]:
        return await repository.list()

    @router.post("/")
    async def create_todo(text: str = Body(..., embed=True)) -> dict[str, UUID]:
        id_ = await repository.insert(text=text)
        return {"id": id_}

    @router.patch("/{id}")
    async def update_todo(
        id_: UUID = Path(..., alias="id"), text: str = Body(..., embed=True)
    ) -> Response:
        result = await repository.edit_text(id_=id_, text=text)

        if result is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.post("/{id}/activate")
    async def activate_todo(id_: UUID = Path(..., alias="id")) -> Response:
        result = await repository.activate(id_=id_)

        if result is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.post("/{id}/deactivate")
    async def deactivate_todo(id_: UUID = Path(..., alias="id")) -> Response:
        result = await repository.deactivate(id_=id_)

        if result is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.delete("/{id}")
    async def delete_todo(id_: UUID = Path(..., alias="id")) -> Response:
        result = await repository.delete(id_)

        if result is None:
            raise HTTPException(status_code=404, detail="Item not found")

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
