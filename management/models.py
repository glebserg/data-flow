from peewee import PostgresqlDatabase, Model, IntegerField, FloatField, DateTimeField, CharField, ForeignKeyField
import datetime
import os

db = PostgresqlDatabase(
    database=os.getenv("POSTGRES_DB"), user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"), port=int(os.getenv("POSTGRES_PORT")), )


class BaseModel(Model):
    """ Базовая модель """
    class Meta:
        database = db


class SensorModel(BaseModel):
    """ Модель сенсора """

    type_sensor = CharField(max_length=20)
    number = IntegerField()

    class Meta:
        db_table = 'sensors'
        indexes = ((('type_sensor', 'number'), True),)


class MetricsModel(BaseModel):
    """ Базовая модель метрик"""

    sensor = ForeignKeyField(SensorModel, on_delete='cascade')
    created = DateTimeField(default=datetime.datetime.now, index=True)

    class Meta:
        abstract = True


class MetricsTemperature(MetricsModel):
    """ Метрики температур """

    class Meta:
        db_table = 'metrics_temperature'

    value = FloatField()


class MetricsHumidity(MetricsModel):
    """ Метрики Влажности """

    class Meta:
        db_table = 'metrics_humidity'

    value = FloatField()


class MetricsCarbonDioxide(MetricsModel):
    """ Метрики CO2(Углекислый газ) """

    class Meta:
        db_table = 'metrics_carbon_dioxide'

    value = IntegerField()
