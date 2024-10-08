import os
from fastapi import FastAPI
from .routes import router
from .config.config import load_config

config_file = "config.yaml"
path = os.path.join("app", "config")
config = load_config(os.path.join(path, config_file))

app = FastAPI()
app.include_router(router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.server.host, port=config.server.port)