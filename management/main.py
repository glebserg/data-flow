#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import Literal, Union
from datetime import datetime
from fastapi import FastAPI, Body, Depends
from models import db, SensorModel, MetricsModel
from dependencies import get_cls_metrics, get_sensor_by_number, get_metrics_obj
from schemas import Item
import requests

app = FastAPI()


@app.get("/runtime/{type_sensors}/sensors")
async def get_runtime_metrics_full(type_sensors: Literal["temperature", "humidity", "carbon-dioxide"]):
    """ Получение текущих метрик всех датчиков """

    resp = requests.get(f"http://{os.getenv('GENERATOR_HOST')}:5000/sensors/{type_sensors}/")
    return resp.json()


@app.post("/db/{type_sensors}/{number_sensor}")
async def record_to_db(item: Item, metrics_cls=Depends(get_cls_metrics), sensor=Depends(get_sensor_by_number), ):
    """ Запись в БД """

    metrics_cls.create(sensor=sensor, value=item.value, created=datetime.fromtimestamp(item.created))
    return {"result": "Recorded"}


@app.get("/db/{type_sensors}/{number_sensor}")
async def get_range_metrics(start: int, end: int, metrics_cls=Depends(get_cls_metrics),
                            sensor=Depends(get_sensor_by_number)):
    """ Чтение БД """

    start_dt, end_dt = datetime.fromtimestamp(start), datetime.fromtimestamp(end)
    result = list(metrics_cls.select().where(
        (metrics_cls.sensor == sensor),
        ((metrics_cls.created > start_dt) & (metrics_cls.created < end_dt))))

    return {"result": {
        metric_obj.id: {"value": metric_obj.value, "created": metric_obj.created} for metric_obj in result
    }
    }


@app.put("/db/{type_sensors}/{number_sensor}")
async def update_metrics_by_id(metrics_obj: MetricsModel = Depends(get_metrics_obj),
                               value: Union[int, float] = Body(embed=True)):
    """ Обновление БД """

    metrics_obj.value = value
    metrics_obj.save()
    return {"result": "Updated"}


@app.delete("/db/{type_sensors}/{number_sensor}")
async def delete_metrics_by_id(metrics_obj: MetricsModel = Depends(get_metrics_obj)):
    """ Обновление БД """

    metrics_obj.delete_instance()
    return {"result": "Deleted"}


@app.on_event("startup")
def generate_values():
    all_tables = MetricsModel.__subclasses__() + [SensorModel]
    db.create_tables(all_tables)
