from pydantic import BaseModel


class SensorBase(BaseModel):
    title: str
    unit: str
    number: int


class SensorTemperature(SensorBase):
    title: str = "Датчик температуры"
    unit: str = "cоставляет [{}] процента"
    value: float = None


class SensorHumidity(SensorBase):
    title: str = "Датчик влажности"
    unit: str = "cоставляет [{}] процента"
    value: float = None


class SensorCarbonDioxide(SensorBase):
    title: str = "Датчик СO2"
    unit: str = "показывает содержание СО2: [{}] ppm"
    value: int = None
