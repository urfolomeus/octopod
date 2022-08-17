import json
import pandas as pd

from src.DataFetcher import DataFetcher

INSTALL_DATE = "2022-08-02T08:00:00"

start_date = INSTALL_DATE

response = DataFetcher().fetch_electricity(start_date)

results = json.loads(response.text)["results"]

df = pd.read_json(json.dumps(results))

print(df)
