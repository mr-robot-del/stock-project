from django.urls import path
from .views import (
    PortfolioListCreateView, PortfolioDetailView,
    PortfolioStockListCreateView, PortfolioStockDetailView
)

urlpatterns = [
    path('', PortfolioListCreateView.as_view(), name='portfolio-list-create'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('<int:portfolio_id>/stocks/', PortfolioStockListCreateView.as_view(), name='portfolio-stock-list-create'),
    path('<int:portfolio_id>/stocks/<int:pk>/', PortfolioStockDetailView.as_view(), name='portfolio-stock-detail'),
]