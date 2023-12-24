from pydantic import BaseModel, Field
from typing import Union, Optional
from datetime import datetime


def get_current_datetime() -> int:
    """ Функция возвращает текущее время """
    return int(datetime.now().timestamp())


class Item(BaseModel):
    """ Модель добавления значения в БД"""
    value: Union[int, float]
    created: Optional[int] = Field(default_factory=get_current_datetime)
