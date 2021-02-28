from django.db import models


class Series(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Values(models.Model):
    dt = models.DateField()
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f"[{self.dt}, {self.series}, {self.value}]"

    class Meta:
        unique_together = [["dt", "series"]]

# Create your models here.
