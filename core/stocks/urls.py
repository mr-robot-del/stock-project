from django.urls import path
from .views import StockSearchView, StockDataViewSet, PredictionViewSet

urlpatterns = [
    path('search/', StockSearchView.as_view(), name='stock-search'),
    path('stockdata/', StockDataViewSet.as_view({'get': 'list', 'post': 'create'}), name='stockdata-list'),
    path('stockdata/<int:pk>/', StockDataViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='stockdata-detail'),
    path('<int:stock_pk>/stockdata/', StockDataViewSet.as_view({'get': 'list'}), name='stock-stockdata-list'),
    path('<int:stock_pk>/stockdata/<int:pk>/', StockDataViewSet.as_view({'get': 'retrieve'}), name='stock-stockdata-detail'),
    path('predictions/', PredictionViewSet.as_view({'get': 'list', 'post': 'create'}), name='prediction-list'),
    path('predictions/<int:pk>/', PredictionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='prediction-detail'),
]