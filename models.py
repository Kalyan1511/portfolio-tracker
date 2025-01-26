from django.db import models
class Stock(models.Model):
    name=models.CharField(max_length=255)
    ticker=models.CharField(max_length=20)
    quantity=models.IntegerField()
    buy_price=models.FloatField()
    current_price=models.FloatField()

    def _str_(self):
        return f"{self.name} ({self.ticker})"


# Create your models here.
