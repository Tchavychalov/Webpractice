import os
import aiofiles
from abc import ABC, abstractmethod
from .nn_model import predict

# абстрактный класс
class Balance(ABC):
    # конструктор
    def __init__(self, token: str):
        self.token = token
        self.balance_file = None
    # абстрактные геттер и сеттер
    @abstractmethod
    async def get_balance(self) -> int:
        pass

    @abstractmethod
    async def set_balance(self, balance: int):
        pass

class FileBalance(Balance):
    # конструктор
    def __init__(self, token: str, path: str="."):
        super().__init__(token)
        self._balance_file = os.path.join(path, f"{token}_balance.txt")
    # геттер
    async def get_balance(self) -> int:
        # проверка существования файла
        if not os.path.exists(self._balance_file):
            return 0
        # TODO нужно, чтобы при несуществующем файле возникала ошибка
        # чтение файла
        async with aiofiles.open(self._balance_file, 'r') as file:
            balance = await file.read()
        # проверка содержимого файла (должны быть только цифры)
        if not balance.isalnum():
            return 0
        # TODO опять-таки - нужно, чтобы возникала ошибка
        return int(balance)
    
    async def set_balance(self, balance: int):
        async with aiofiles.open(self._balance_file, 'w') as file:
            await file.write(str(balance))
        

# Обработка файлов
class FileService:
    # Конструктор
    def __init__(self, path: str="."):
        self.path = path
    
    #Метод для чтения содержимого файла
    async def get_file_content(self, file_name: str) -> str:
        async with aiofiles.open(os.path.join(self.path, file_name), 'r') as file:
            return await file.read()
            
    
    # Метод для записи файла
    async def set_file_content(self, file_name: str, content: str):
        async with aiofiles.open(os.path.join(self.path, file_name), 'w') as file:
            await file.write(content)
    
    # Метод для уменьшения баланса
    async def balance_dec(self, file_name: str, price: int=10):
        balance = await self.get_file_content(file_name)
        balance = int(balance)
        balance -= price
        await self.set_file_content(file_name, str(balance))
    
    # Метод для проверки существования файла
    def file_exists(self, file_name: str) -> bool:
        return os.path.exists(os.path.join(self.path, file_name))
    
    # Метод для удаления файла
    def delete_file(self, file_name: str):
        os.remove(os.path.join(self.path, file_name))


class NNService:
    async def run_nn(self, query: str) -> str:
        res_dict = {0: "Neutral", 1: "Positive", 2: "Negative"}
        res = predict(query)  # результат предсказания
        return f'Запрос: {query}\nРезультат:{res_dict[res[0]]}'