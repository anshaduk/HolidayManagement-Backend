from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    country_code = models.CharField(max_length=10)
    date = models.DateField()
    type = models.CharField(max_length=50)
    year = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['country_code','year']),
            models.Index(fields=['name']),
        ]


