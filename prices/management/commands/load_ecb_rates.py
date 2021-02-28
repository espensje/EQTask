import requests
import datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from prices.src.timeseries_loader import TimeSeriesLoader


URL = r"https://app.energyquantified.com/static/data/ecb_reference_rates_90d.xml"
SERIES_NAME = "EUR/USD"     # only one series here


class Command(TimeSeriesLoader, BaseCommand):
    help = "Loads EUR/USD exchange rates from the European Central Bank."

    def _get_data(self):
        with requests.Session() as session:
            res = session.get(URL)

        return BeautifulSoup(res.content, "xml")

    def _parse_data(self, data):
        series, values = [], []
        root = data.find("Cube")
        for timeseries in root.find_all("Cube", recursive=False):
            dt = datetime.datetime.strptime(timeseries["time"], "%Y-%m-%d").date()
            value = float(timeseries.find("Cube", currency="USD")["rate"])
            values.append({"series_name": SERIES_NAME, "dt": dt, "value": value})

        return series, values

    def handle(self, *args, **options):
        _, values = self._parse_data(self._get_data())
        self._save_series([{"name": SERIES_NAME}])
        self._save_values(values)



