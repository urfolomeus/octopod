import json

from src.connection import Connection
from src.DataFetcher import DataFetcher

db = Connection()


def record_electricity():
    last_recorded_date = db.get_last_recorded_date("elec")
    print(f"Fetching data recorded since {last_recorded_date}")
    response = DataFetcher().fetch_electricity(last_recorded_date)
    results = json.loads(response.text)["results"]

    if len(results):
        db.write(results, "elec")


def read_electricity():
    readings = db.read()
    print(readings.sort_values("interval_start", ascending=False))


record_electricity()
read_electricity()
