from prices.models import Series, Values
from django.views.generic import TemplateView, ListView


# Create your views here.
class IndexView(ListView):
    series_list = Series

    def get_queryset(self):
        return Series.objects.all().order_by("id")


class GetView(TemplateView):

    @staticmethod
    def _get_rate_values_as_dict():
        rate_series = Series.objects.get(name="EUR/USD")
        rate_values = Values.objects.filter(series=rate_series).values()
        rate_values_dict = dict()
        for rv in rate_values:
            rate_values_dict[rv["dt"]] = rv["value"]

        return rate_values_dict

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = Series.objects.get(id=int(context["series_id"]))
        context["series"] = series
        timeseries = Values.objects.filter(series=series).order_by("-dt").values()
        context["exchangerate"] = True if "EUR/" in series.name else False
        if not context["exchangerate"]:
            rate_values = self._get_rate_values_as_dict()
            for ts in timeseries:
                if ts["dt"] in rate_values.keys():
                    ts["value_eur"] = round(ts["value"] / rate_values[ts["dt"]], 2)
                else:
                    ts["value_eur"] = "-"

        context["timeseries"] = timeseries

        return context


