import json

from src.connection import Connection
from src.DataFetcher import DataFetcher

db = Connection()


def record_consumption(consumption_type):
    last_recorded_date = db.get_last_recorded_date(consumption_type)
    print(f"Fetching data recorded since {last_recorded_date}...")
    response = DataFetcher().fetch(consumption_type, last_recorded_date)
    results = json.loads(response.text)["results"]
    print(f"Received {len(results)} readings\n")
    if len(results):
        db.write(results, consumption_type)


def read_consumption(consumption_type):
    readings = db.read(consumption_type)
    print(readings.sort_values("interval_start", ascending=False))


print("Electricity")
print("-----------")
record_consumption("elec")
read_consumption("elec")

print("\n\n")

print("Gas")
print("---")
record_consumption("gas")
read_consumption("gas")
