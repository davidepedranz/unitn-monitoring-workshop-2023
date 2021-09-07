from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    cleanup_timeout_seconds: int = Field(default=10)
    postgresql_connection_url: SecretStr = Field(
        default="postgres://postgres:password@localhost:5432/postgres"
    )
    postgresql_min_connections: int = Field(default=1)
    postgresql_max_connections: int = Field(default=10)
    prometheus_host: str = Field(default="0.0.0.0")
    prometheus_port: int = Field(default=5001)
