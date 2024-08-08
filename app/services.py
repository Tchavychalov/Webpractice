import os
import aiofiles
from .nn_model import predict

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