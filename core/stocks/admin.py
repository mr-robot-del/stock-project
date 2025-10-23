from django.contrib import admin
from .models import Stock, StockData, Prediction

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'name', 'sector']
    search_fields = ['ticker', 'name']

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ['stock', 'date', 'close', 'volume']
    list_filter = ['stock', 'date']
    search_fields = ['stock__ticker']

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['stockdata', 'moving_average', 'computed_at']
    list_filter = ['computed_at']