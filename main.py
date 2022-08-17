import json
import os
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth


BASE_URL = "https://api.octopus.energy/v1"
MPAN = os.environ["OCTOPUS_MPAN"]
SERIAL_NUMBER_ELEC = os.environ["OCTOPUS_SERIAL_ELEC"]
PAGE_SIZE = 1000

url = f"{BASE_URL}/electricity-meter-points/{MPAN}/meters/{SERIAL_NUMBER_ELEC}/consumption?page_size={PAGE_SIZE}"

# Octopus just provide an API token and expect that to be provided as a Basic Auth user
# HTTPBasicAuth expects a password too, so we just use an empty string
basic = HTTPBasicAuth(os.environ["OCTOPUS_TOKEN"], "")

response = requests.request("GET", url, auth=basic)

results = json.loads(response.text)["results"]

df = pd.read_json(json.dumps(results))

print(df)
