from datetime import datetime
from loguru import logger
import asyncio
import random
from abc import ABC
from schemes import SensorBase, SensorTemperature, SensorHumidity, SensorCarbonDioxide
from typing import Union


class GeneratorBase(ABC):

    def __init__(self, scheme: SensorBase, count: int, range_values: tuple, frequency: int, ) -> None:
        self.count = count
        self.range_values = range_values
        self.frequency = frequency
        self.sensors = [scheme(number=num) for num in range(1, self.count + 1)]

    def __get_value(self, sensor_obj: SensorBase) -> Union[float, int]:
        if sensor_obj.__class__.__annotations__["value"] is float:
            return round(random.uniform(self.range_values[0], self.range_values[1]), 2)
        else:
            return int(random.randint(self.range_values[0], self.range_values[1]))

    async def generate(self) -> None:
        while True:
            for sensor_obj in self.sensors:
                sensor_obj.value = self.__get_value(sensor_obj)
                logger.info(f"{sensor_obj.title} [{sensor_obj.number}] в момент времени ["
                            f"{datetime.now():%d-%m-%Y %H:%M:%S}] "
                            f"{sensor_obj.unit.format(sensor_obj.value)}")
            await asyncio.sleep(self.frequency)


class GeneratorTemperatures(GeneratorBase):

    def __init__(self, scheme: SensorTemperature, count: int, range_values: tuple, frequency: int):
        super().__init__(scheme, count, range_values, frequency)


class GeneratorHumidity(GeneratorBase):

    def __init__(self, scheme: SensorHumidity, count: int, range_values: tuple, frequency: int):
        super().__init__(scheme, count, range_values, frequency)


class GeneratorCarbonDioxide(GeneratorBase):

    def __init__(self, scheme: SensorCarbonDioxide, count: int, range_values: tuple, frequency: int):
        super().__init__(scheme, count, range_values, frequency)
