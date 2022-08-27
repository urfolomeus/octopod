import os
import requests

BASE_URL = "https://api.octopus.energy/v1"
PAGE_SIZE = 10000


class DataFetcher:
    def fetch(self, consumption_type, last_recorded_date):
        url = None
        if consumption_type == "elec":
            url = self.__electricity_url(last_recorded_date)
        elif consumption_type == "gas":
            url = self.__gas_url(last_recorded_date)

        return requests.request("GET", url, auth=self.__basic())

    def __electricity_url(self, last_recorded_date):
        mpan = os.environ["OCTOPUS_MPAN"]
        serial = os.environ["OCTOPUS_SERIAL_ELEC"]
        return (
            f"{BASE_URL}/electricity-meter-points/{mpan}/meters/{serial}"
            f"/consumption?period_from={last_recorded_date}&page_size={PAGE_SIZE}"
        )

    def __gas_url(self, last_recorded_date):
        mpan = os.environ["OCTOPUS_MPRN"]
        serial = os.environ["OCTOPUS_SERIAL_GAS"]
        return (
            f"{BASE_URL}/gas-meter-points/{mpan}/meters/{serial}"
            f"/consumption?period_from={last_recorded_date}&page_size={PAGE_SIZE}"
        )

    def __basic(self):
        # Octopus just provide an API token and expect that to be provided as
        # a Basic Auth user. HTTPBasicAuth expects a password too, so we just
        # use an empty string.
        return requests.auth.HTTPBasicAuth(os.environ["OCTOPUS_TOKEN"], "")
