from typing import Optional, List

from pydantic import BaseModel


class SetWebhookArguments(BaseModel):
    url: str
    certificate: Optional[str]  # Path
    ip_address: Optional[str]
    max_connections: Optional[int]
    allowed_updates: Optional[List[str]]
    drop_pending_updates: Optional[bool]
    secret_token: Optional[str]


class WebhookAppSettings(BaseModel):
    host: str
    port: int
    path: str
    workers: Optional[int]
    ssl_keyfile: Optional[str]
    ssl_certfile: Optional[str]
    ssl_keyfile_password: Optional[str]


class WebhookConfig(BaseModel):
    arguments: SetWebhookArguments
    app_options: WebhookAppSettings


class Config(BaseModel):
    alembic_connection_string: str
    bot_connection_string: str
    bot_token: str
    webhook: Optional[WebhookConfig]
