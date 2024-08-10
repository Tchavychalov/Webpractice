import os
import aiofiles

class FileService:
    def __init__(self, path=".") -> None:
        self.path = path
    # Проверка существования файла
    def exist_file(self, file: str) -> bool:
        
        if os.path.exists(os.path.join(self.path, file)):
            return True
        else:
            return False
    # Запись в файл
    async def set_file_content(self, file: str, content: str) -> None:
        async with aiofiles.open(os.path.join(self.path, file), 'w') as f:
            await f.write(str(content))
    # Чтение из файла
    async def get_file_content(self, file: str) -> str:
        if self.exist_file(file):
            async with aiofiles.open(os.path.join(self.path, file), 'r') as f:
                return await f.read()
        else:
            raise FileNotFoundError
    # Удаление файла
    async def delete_file(self, file: str) -> None:
        if self.exist_file(file):
            os.remove(os.path.join(self.path, file))
        else:
            raise FileNotFoundError
    