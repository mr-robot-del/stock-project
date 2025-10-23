from django.shortcuts import render
import requests
from django.conf import settings
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from .models import Stock, StockData, Prediction
from .serializers import StockSerializer, StockDataSerializer, PredictionSerializer
from datetime import datetime
from decimal import Decimal
from rest_framework.views import APIView

def fetch_alpha_vantage_data(ticker):
    """Fetch daily time-series from Alpha Vantage."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        time_series = data.get('Time Series (Daily)', {})
        if 'Error Message' in data or not time_series:
            return None, {'error': 'Invalid ticker or no data available'}
        return time_series, None
    except requests.RequestException as e:
        return None, {'error': f"API request failed: {str(e)}"}
class StockSearchView(APIView):
    """
    Search stocks by ticker, name, or sector using Alpha Vantage or local DB.
    Query params: ?ticker=AAPL or ?name=Apple or ?sector=Technology
    """
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):
        ticker = request.query_params.get('ticker', '').strip().upper()
        name = request.query_params.get('name', '').strip()
        sector = request.query_params.get('sector', '').strip()

        if not any([ticker, name, sector]):
            return Response({'error': 'Provide ticker, name, or sector query param'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Stock.objects.all()
        if ticker:
            queryset = queryset.filter(ticker__icontains=ticker)
        elif name:
            queryset = queryset.filter(name__icontains=name)
        elif sector:
            queryset = queryset.filter(sector__icontains=sector)

        if queryset.exists():
            serializer = StockSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if ticker or name:
            query = ticker or name
            url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                matches = data.get('bestMatches', [])

                if not matches:
                    return Response({'error': 'No matches found'}, status=status.HTTP_404_NOT_FOUND)

                results = []
                for match in matches[:10]:
                    stock_data = {
                        'ticker': match['1. symbol'],
                        'name': match['2. name'],
                        'sector': 'Unknown'
                    }
                    stock, created = Stock.objects.get_or_create(
                        ticker=stock_data['ticker'],
                        defaults={'name': stock_data['name'], 'sector': stock_data['sector']}
                    )
                    if created:
                        meta_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_data['ticker']}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
                        try:
                            meta_response = requests.get(meta_url, timeout=5).json()
                            stock.sector = meta_response.get('Sector', 'Unknown')
                            stock.save()
                        except:
                            pass
                    results.append(StockSerializer(stock).data)

                return Response(results, status=status.HTTP_200_OK)

            except requests.RequestException as e:
                return Response({'error': f"API request failed: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({'error': 'No local stocks in this sector.'}, status=status.HTTP_404_NOT_FOUND)

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        ticker = request.query_params.get('ticker', '').strip().upper()
        name = request.query_params.get('name', '').strip()
        sector = request.query_params.get('sector', '').strip()

        if not any([ticker, name, sector]):
            return Response({'error': 'Provide ticker, name, or sector query param'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Stock.objects.all()
        if ticker:
            queryset = queryset.filter(ticker__icontains=ticker)
        elif name:
            queryset = queryset.filter(name__icontains=name)
        elif sector:
            queryset = queryset.filter(sector__icontains=sector)

        if queryset.exists():
            serializer = StockSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if ticker or name:
            query = ticker or name
            url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                matches = data.get('bestMatches', [])

                if not matches:
                    return Response({'error': 'No matches found'}, status=status.HTTP_404_NOT_FOUND)

                results = []
                for match in matches[:10]:
                    stock_data = {
                        'ticker': match['1. symbol'],
                        'name': match['2. name'],
                        'sector': 'Unknown'
                    }
                    stock, created = Stock.objects.get_or_create(
                        ticker=stock_data['ticker'],
                        defaults={'name': stock_data['name'], 'sector': stock_data['sector']}
                    )
                    if created:
                        meta_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock_data['ticker']}&apikey={settings.ALPHA_VANTAGE_API_KEY}"
                        try:
                            meta_response = requests.get(meta_url, timeout=5).json()
                            stock.sector = meta_response.get('Sector', 'Unknown')
                            stock.save()
                        except:
                            pass
                    results.append(StockSerializer(stock).data)

                return Response(results, status=status.HTTP_200_OK)

            except requests.RequestException as e:
                return Response({'error': f"API request failed: {str(e)}"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({'error': 'No local stocks in this sector. Pre-populate DB or use premium API.'}, status=status.HTTP_404_NOT_FOUND)

class StockDataViewSet(viewsets.ModelViewSet):
    queryset = StockData.objects.all()
    serializer_class = StockDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        stock_id = self.kwargs.get('stock_id')
        if stock_id:
            queryset = queryset.filter(stock_id=stock_id)
        return queryset

    def list(self, request):
        stock_id = request.query_params.get('stock_id') or self.kwargs.get('stock_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not stock_id:
            return Response({'error': 'stock_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            stock = Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)

        queryset = self.queryset.filter(stock=stock)
        if start_date:
            try:
                queryset = queryset.filter(date__gte=datetime.strptime(start_date, '%Y-%m-%d').date())
            except ValueError:
                return Response({'error': 'Invalid start_date format (use YYYY-MM-DD)'}, status=status.HTTP_400_BAD_REQUEST)
        if end_date:
            try:
                queryset = queryset.filter(date__lte=datetime.strptime(end_date, '%Y-%m-%d').date())
            except ValueError:
                return Response({'error': 'Invalid end_date format (use YYYY-MM-DD)'}, status=status.HTTP_400_BAD_REQUEST)

        if not queryset.exists():
            time_series, error = fetch_alpha_vantage_data(stock.ticker)
            if error:
                return Response(error, status=status.HTTP_400_BAD_REQUEST)

            for date_str, values in time_series.items():
                StockData.objects.update_or_create(
                    stock=stock,
                    date=datetime.strptime(date_str, '%Y-%m-%d').date(),
                    defaults={
                        'open': Decimal(values['1. open']),
                        'high': Decimal(values['2. high']),
                        'low': Decimal(values['3. low']),
                        'close': Decimal(values['4. close']),
                        'volume': int(values['5. volume'])
                    }
                )
            queryset = self.queryset.filter(stock=stock)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class PredictionViewSet(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        stockdata = serializer.validated_data['stockdata']
        recent_data = StockData.objects.filter(
            stock=stockdata.stock,
            date__lte=stockdata.date
        ).order_by('-date')[:7]
        if len(recent_data) < 7:
            raise serializers.ValidationError('Not enough data for 7-day moving average')
        moving_average = sum(Decimal(str(d.close)) for d in recent_data) / len(recent_data)
        serializer.save(moving_average=moving_average, other_metrics=None)