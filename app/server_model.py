from pydantic import BaseModel

class ServerConfig(BaseModel):
    host: str
    port: int

class AppConfig(BaseModel):
    server: ServerConfig
    env: str = "local"