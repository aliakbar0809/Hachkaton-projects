from django.db import models

class CurrencyRate(models.Model):
    currency = models.CharField(max_length=10)
    buy_rate = models.FloatField()
    sell_rate = models.FloatField()
    date = models.DateField()
