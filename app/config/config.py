import yaml
from pydantic import ValidationError
from ..server_model import AppConfig

def load_config(path: str) -> AppConfig:
    try:
        with open(path, "r") as file:
            config_data = yaml.safe_load(file)
            return AppConfig(**config_data)
    except FileNotFoundError:
        raise BaseException(f"Config file {path} not found")
    except Exception as ex:
        raise BaseException(f"Error: {ex}")