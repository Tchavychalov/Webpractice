from fastapi import BackgroundTasks

from ..models import MLRequest, new_token
from .balance_service import FileBalance
from .nn_service import NNService
from .file_service import FileService

class TaskAddService:
    def __init__(self, balance_service: FileBalance, nn_service: NNService, file_service: FileService) -> None:
        self.balance_service = balance_service
        self.nn_service = nn_service
        self.file_service = file_service
        print("Конструктор TaskAddService")
    
    async def add_task(self, request: MLRequest, background: BackgroundTasks) -> str:
        print(f"В add_task получены {request.token} и {request.query}")
        # считать баланс и проверить его
        balance = await self.balance_service.get_balance()
        if balance < 10:
            raise NotEnoughBalanceError("Недостаточный баланс")
        # генерация ID задачи, временного файла и файла с результатами
        req_id = new_token(4)
        wait_filename = f"{request.token}_{req_id}_wait.txt"
        done_filename = f"{request.token}_{req_id}_ready.txt"
        # создание временного файла
        await self.file_service.set_file_content(wait_filename, "")
        # уменьшение баланса
        await self.balance_service.set_balance(balance - 10)
        # запуск обработки в бэкграунде
        background.add_task(self.process_task, request, done_filename, wait_filename)
        return req_id
    
    # метод для передачи запроса в нейронную сеть
    async def process_task(self, request: MLRequest, done_filename: str, wait_filename: str) -> None:
        result = await self.nn_service.run_nn(request.query)
        await self.file_service.set_file_content(done_filename, result)
        await self.file_service.delete_file(wait_filename)


class TaskResultService:
    def __init__(self, file_service: FileService, nn_service: NNService):
        self.file_service = file_service
        self.nn_service = nn_service
    
    async def get_result(self, token, req_id: str) -> dict:
        wait_filename = f"{token}_{req_id}_wait.txt"
        done_filename = f"{token}_{req_id}_ready.txt"

        if not self.file_service.exist_file(done_filename) and self.file_service.exist_file(wait_filename):
            raise TaskNotDoneError("Запрос отправлен, обработка еще не выполнена")
        if not self.file_service.exist_file(done_filename):
            raise TaskNotFoundError("Запрос не найден")
        
        result = await self.file_service.get_file_content(done_filename)
        return {'result': result}
        


class NotEnoughBalanceError(Exception):
    pass

class TaskNotDoneError(Exception):
    pass

class TaskNotFoundError(Exception):
    pass