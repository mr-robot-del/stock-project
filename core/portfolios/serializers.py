from rest_framework import serializers
from .models import Portfolio, PortfolioStock
from stocks.models import Stock
import requests
from django.conf import settings

class PortfolioStockSerializer(serializers.ModelSerializer):
    stock_ticker = serializers.CharField(source='stock.ticker', read_only=True)
    stock_name = serializers.CharField(source='stock.name', read_only=True)
    ticker = serializers.CharField(write_only=True, help_text="Stock ticker to add (fetched from API)")

    class Meta:
        model = PortfolioStock
        fields = ['id', 'ticker', 'stock_ticker', 'stock_name', 'quantity', 'buy_price', 'buy_date']

    def create(self, validated_data):
        ticker = validated_data.pop('ticker')
        portfolio_id = self.context['portfolio_id']
        portfolio = Portfolio.objects.get(id=portfolio_id)

        stock = Stock.objects.filter(ticker__iexact=ticker).first()
        if not stock:
            # Fetch from API
            url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
            response = requests.get(url)
            data = response.json()
            matches = data.get('bestMatches', [])
            if not matches or matches[0]['1. symbol'].upper() != ticker.upper():
                raise serializers.ValidationError(f"Invalid ticker '{ticker}'. No match found.")
            match = matches[0]
            stock = Stock.objects.create(
                ticker=match['1. symbol'],
                name=match['2. name'],
                sector='Unknown'
            )

        validated_data['stock'] = stock
        validated_data['portfolio'] = portfolio
        return super().create(validated_data)

class PortfolioSerializer(serializers.ModelSerializer):
    total_invested = serializers.SerializerMethodField(read_only=True)
    portfolio_stocks = PortfolioStockSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ['id', 'name', 'description', 'created_at', 'total_invested', 'portfolio_stocks']

    def get_total_invested(self, obj):
        return obj.get_total_invested()