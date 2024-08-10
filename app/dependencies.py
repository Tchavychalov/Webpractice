from .services.file_service import FileService
from .services.nn_service import NNService
from .services.balance_service import FileBalance

def get_file_service() -> FileService:
    return FileService()

def get_nn_service() -> NNService:
    return NNService()

def get_balance_service(token: str) -> FileBalance:
    return FileBalance(token)