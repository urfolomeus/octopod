import os
import requests

BASE_URL = "https://api.octopus.energy/v1"
PAGE_SIZE = 1000


class DataFetcher:
    def fetch_electricity(self, last_recorded_date):
        mpan = os.environ["OCTOPUS_MPAN"]
        serial = os.environ["OCTOPUS_SERIAL_ELEC"]
        url = (
            f"{BASE_URL}/electricity-meter-points/{mpan}/meters/{serial}"
            f"/consumption?period_from={last_recorded_date}&page_size={PAGE_SIZE}"
        )

        return requests.request("GET", url, auth=self.__basic())

    def __basic(self):
        # Octopus just provide an API token and expect that to be provided as
        # a Basic Auth user. HTTPBasicAuth expects a password too, so we just
        # use an empty string.
        return requests.auth.HTTPBasicAuth(os.environ["OCTOPUS_TOKEN"], "")
