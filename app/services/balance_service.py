import os
import aiofiles
from abc import ABC, abstractmethod

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
        print(f"get_balance {self._balance_file}")
        if not os.path.exists(self._balance_file):
            await self.set_balance(100)
        # чтение файла
        async with aiofiles.open(self._balance_file, 'r') as file:
            balance = await file.read()
        return int(balance)
    
    async def set_balance(self, balance: int):
        async with aiofiles.open(self._balance_file, 'w') as file:
            await file.write(str(balance))
        
