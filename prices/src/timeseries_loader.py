from abc import ABC, abstractmethod
from prices.models import Series, Values


class TimeSeriesLoader(ABC):

    @abstractmethod
    def _get_data(self):
        pass

    def _parse_data(self, data):
        """
        Reference the relevant value's series as key-value 'series_name': name of series
        :param data:
        :return: Lists of dicts
        """
        series, values = [], []
        return series, values

    @staticmethod
    def _save_series(series):
        """
        Insert new series to database.
        :param series: List of dicts
        :return:
        """
        for entry in series:
            obj, _ = Series.objects.get_or_create(**entry)
            obj.save()

    @staticmethod
    def _save_values(values):
        """
        Insert/update values to database.
        :param values: List of dicts
        :return:
        """
        for entry in values:
            series = Series.objects.get(name=entry.get("series_name"))
            obj, _ = Values.objects.get_or_create(**{"series": series,
                                                     "dt": entry.get("dt"),
                                                     "value": entry.get("value")})
            obj.save()
