'''В файле описаны модели (запрос оценки отзыва, ответ, текущий баланс) и генерация токена'''
import string
import random
from pydantic import BaseModel, Field, field_validator

# Модель запроса к нейронной сети
class MLRequest(BaseModel):
    token: str = Field(..., pattern="^[a-zA-Z]{8}$")
    query: str
    # Валидация токена
    @field_validator("token")
    def validate_token(cls, token):
        if len(token) != 8 or not token.isalpha():
            raise ValueError('Токен должен состоять из 8 символов латинницы')
        return token


# Функция генерации нового токена
def new_token(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))