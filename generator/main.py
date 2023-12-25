#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import asyncio
from fastapi import FastAPI
from generators import GeneratorTemperatures, GeneratorHumidity, GeneratorCarbonDioxide
from loguru import logger
from schemes import SensorTemperature, SensorHumidity, SensorCarbonDioxide
from typing import Literal

app = FastAPI()

logger.remove()
logger.add(sys.stdout, format="{message}", level="INFO")
logger.add("logger.log", format="{message}", rotation="1 week", level="INFO")

temperature = GeneratorTemperatures(scheme=SensorTemperature, count=8, range_values=(10, 65), frequency=10)
humidity = GeneratorHumidity(scheme=SensorHumidity, count=2, range_values=(10, 99), frequency=2)
carbon_dioxide = GeneratorCarbonDioxide(scheme=SensorCarbonDioxide, count=2, range_values=(0, 5000), frequency=5)

storage = {
    "temperature": temperature,
    "humidity": humidity,
    "carbon-dioxide": carbon_dioxide,
}


@app.get("/sensors/{type_sensors}/")
async def get_data(type_sensors: Literal["temperature", "humidity", "carbon-dioxide"]):
    """ Функция возвразает метрики по каждому сенсору в зависимости от типа сенсора """
    return {"result": {sensor.number: sensor.value for sensor in storage[type_sensors].sensors}}


@app.on_event("startup")
def begin_generators():
    for type_sensors in storage.keys():
        asyncio.create_task(storage[type_sensors].generate())
