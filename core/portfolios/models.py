from django.db import models
from django.contrib.auth import get_user_model
from stocks.models import Stock
from decimal import Decimal
from datetime import date

User = get_user_model()

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    def get_total_invested(self):
        return sum(ps.quantity * ps.buy_price for ps in self.portfolio_stocks.all())

class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='portfolio_stocks')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_date = models.DateField(default=date.today)

    class Meta:
        unique_together = ('portfolio', 'stock')
    def __str__(self):
        return f"{self.portfolio.name} - {self.stock.ticker} ({self.quantity} shares @ ${self.buy_price})"