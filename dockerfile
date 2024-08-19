# 1. Используем официальный базовый образ Python 3.11
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем все файлы проекта в контейнер
COPY . .

# 6. Устанавливаем переменные окружения для работы FastAPI в Uvicorn
ENV CONFIG_PATH=/app/config/config.yaml

# 7. Указываем команду для запуска приложения (Uvicorn) с чтением конфигурации из файла
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

