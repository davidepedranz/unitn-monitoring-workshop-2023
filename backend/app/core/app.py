from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client.exposition import start_http_server as run_prometheus_http_server

from app.config import Config
from app.core.api import create_todos_router
from app.dependencies import Dependencies, setup_dependencies


def create_app() -> FastAPI:
    """
    Load the configuration, prepare the dependencies, and initialize the FastAPI app.
    """
    config = Config()
    dependencies = setup_dependencies(config)

    run_prometheus_http_server(addr=config.prometheus_host, port=config.prometheus_port)

    return _make_fastapi_app(config=config, dependencies=dependencies)


def _make_fastapi_app(config: Config, dependencies: Dependencies) -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)

    app.add_middleware(CORSMiddleware, allow_origins="*", allow_methods="*")
    app.include_router(create_todos_router(repository=dependencies.repository))

    @app.on_event("startup")
    async def _startup() -> None:
        await dependencies.init()

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await dependencies.shutdown(config.cleanup_timeout_seconds)

    return app
