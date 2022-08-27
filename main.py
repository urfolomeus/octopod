import json

from src.connection import Connection
from src.DataFetcher import DataFetcher

db = Connection()


def record_electricity():
    last_recorded_date = db.get_last_recorded_date("elec")
    print(f"Fetching data recorded since {last_recorded_date}...")
    response = DataFetcher().fetch_electricity(last_recorded_date)
    results = json.loads(response.text)["results"]
    print(f"Received {len(results)} readings\n")
    if len(results):
        db.write(results, "elec")


def read_electricity():
    readings = db.read("elec")
    print(readings.sort_values("interval_start", ascending=False))


def record_gas():
    last_recorded_date = db.get_last_recorded_date("gas")
    print(f"Fetching data recorded since {last_recorded_date}...")
    response = DataFetcher().fetch_gas(last_recorded_date)
    results = json.loads(response.text)["results"]
    print(f"Received {len(results)} readings\n")
    if len(results):
        db.write(results, "gas")


def read_gas():
    readings = db.read("gas")
    print(readings.sort_values("interval_start", ascending=False))


print("Electricity")
print("-----------")
record_electricity()
read_electricity()

print("\n\n")

print("Gas")
print("---")
record_gas()
read_gas()
