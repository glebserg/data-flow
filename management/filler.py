import datetime
from typing import Literal, Union
import requests


def save_to_db(type_s: Literal["temperature", "humidity", "carbon-dioxide"],
               number_s: int, value: Union[int, float], created: int) -> None:
    url = f"http://localhost:5002/db/{type_s}/{number_s}/"
    data_json = {"value": value, "created": created}
    r = requests.post(url=url, json=data_json)


def main():
    start = datetime.datetime.now() - datetime.timedelta(days=1)
    types_sensors = ["temperature", "humidity", "carbon-dioxide"]

    while start < datetime.datetime.now():
        start += datetime.timedelta(minutes=1)

        for sensor in types_sensors:
            resp = requests.get(f"http://localhost:5001/sensors/{sensor}/")
            if resp.ok:
                data = resp.json()["result"]
                for number_sensor in data.keys():
                    save_to_db(type_s=sensor, number_s=number_sensor, value=data[number_sensor],
                               created=int(start.timestamp()))
                print(f"Created {start}")


if __name__ == '__main__':
    main()
