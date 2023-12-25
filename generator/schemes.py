from pydantic import BaseModel


class SensorBase(BaseModel):
    """ Модель Сенсора """
    title: str
    unit: str
    number: int


class SensorTemperature(SensorBase):
    """ Модель Сенсора Температуры """
    title: str = "Датчик температуры"
    unit: str = "cоставляет [{}] процента"
    value: float = None


class SensorHumidity(SensorBase):
    """ Модель Сенсора Влажности """
    title: str = "Датчик влажности"
    unit: str = "cоставляет [{}] процента"
    value: float = None


class SensorCarbonDioxide(SensorBase):
    """ Модель Сенсора Влажности """
    title: str = "Датчик СO2"
    unit: str = "показывает содержание СО2: [{}] ppm"
    value: int = None
