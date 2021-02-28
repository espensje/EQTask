import requests
import json
import datetime
from django.core.management.base import BaseCommand
from prices.src.timeseries_loader import TimeSeriesLoader


URL = r"https://app.energyquantified.com/static/data/oil_prices.json"


class Command(TimeSeriesLoader, BaseCommand):
    help = "Loads closing prices from Brent Crude Oil monthly contracts."

    def _get_data(self):
        with requests.Session() as session:
            res = session.get(URL)

        return json.loads(res.text)

    @staticmethod
    def _create_series_name(contract):
        dt = datetime.datetime.strptime(contract, "%B %Y")
        return "M" + dt.strftime("%m") + dt.strftime("%Y")

    def _parse_data(self, data):
        series, values = [], []
        for contract_timeseries in data:
            series_name = self._create_series_name(contract_timeseries["contract"])
            series.append({"name": series_name})
            for timeseries in contract_timeseries.get("data", []):
                dt = datetime.datetime.strptime(timeseries.get("date"), "%Y-%m-%d").date()
                value = float(timeseries.get("price"))
                values.append({"series_name": series_name, "dt": dt, "value": value})

        return series, values

    def handle(self, *args, **options):
        series, values = self._parse_data(self._get_data())
        self._save_series(series)
        self._save_values(values)



