from fastapi import Body, Depends, HTTPException
from typing import Literal, Type
from models import MetricsModel, MetricsTemperature, MetricsHumidity, MetricsCarbonDioxide, SensorModel


def get_sensor_by_number(number_sensor: int, type_sensors: Literal["temperature", "humidity", "carbon-dioxide"]) -> SensorModel:
    """ Функция возвращает объект Сенсора, предварительно создавая, если его нет в БД """
    return SensorModel().get_or_create(type_sensor=type_sensors, number=number_sensor)[0]


def get_cls_metrics(type_sensors: Literal["temperature", "humidity", "carbon-dioxide"]) -> Type[MetricsModel]:
    """ Функция возвращает тип класса Сенсора, в зависимости от ключа """
    match type_sensors:
        case "temperature":
            return MetricsTemperature
        case "humidity":
            return MetricsHumidity
        case "carbon-dioxide":
            return MetricsCarbonDioxide


def get_metrics_obj(metrics_id: int = Body(embed=True), metrics_cls=Depends(get_cls_metrics)) -> MetricsModel:
    metrics_obj = metrics_cls.get_or_none(metrics_cls.id == metrics_id)
    if metrics_obj is None:
        raise HTTPException(status_code=400, detail=f"Metrics with ID {metrics_id} not found")
    else:
        return metrics_obj
