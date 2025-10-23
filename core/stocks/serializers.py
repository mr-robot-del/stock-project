from rest_framework import serializers
from .models import Stock, StockData, Prediction

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'ticker', 'name', 'sector']

class StockDataSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = StockData
        fields = ['id', 'stock', 'date', 'open', 'high', 'low', 'close', 'volume']
        read_only_fields = ['stock']

class PredictionSerializer(serializers.ModelSerializer):
    stockdata = StockDataSerializer(read_only=True)

    class Meta:
        model = Prediction
        fields = ['id', 'stockdata', 'moving_average', 'other_metrics', 'computed_at']
        read_only_fields = ['moving_average', 'other_metrics', 'computed_at']