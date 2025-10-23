from django.db import models
from django.core.validators import MinValueValidator

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100)

    class Meta:
        indexes = [models.Index(fields=['ticker'])]
        ordering = ['ticker']

    def __str__(self):
        return self.ticker

class StockData(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_data')
    date = models.DateField()
    open = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    high = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    low = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    close = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    volume = models.BigIntegerField(validators=[MinValueValidator(0)])

    class Meta:
        unique_together = ('stock', 'date')
        indexes = [models.Index(fields=['stock', 'date'])]
        ordering = ['-date']

    def __str__(self):
        return f"{self.stock.ticker} - {self.date}"

class Prediction(models.Model):
    stockdata = models.ForeignKey(StockData, on_delete=models.CASCADE, related_name='predictions')
    moving_average = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    other_metrics = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    computed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['stockdata'])]
        ordering = ['-computed_at']

    def __str__(self):
        return f"Prediction for {self.stockdata} at {self.computed_at}"
