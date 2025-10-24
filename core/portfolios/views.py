from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, PortfolioStock
from .serializers import PortfolioSerializer, PortfolioStockSerializer

class PortfolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.portfolios.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.portfolios.all()

class PortfolioStockListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioStockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        portfolio_id = self.kwargs['portfolio_id']
        return PortfolioStock.objects.filter(portfolio_id=portfolio_id)

    def get_serializer_context(self):
        """Pass portfolio_id to serializer context for create."""
        context = super().get_serializer_context()
        context['portfolio_id'] = self.kwargs['portfolio_id']
        return context

    def perform_create(self, serializer):
        portfolio = Portfolio.objects.get(id=self.kwargs['portfolio_id'], user=self.request.user)
        serializer.save(portfolio=portfolio)
        
class PortfolioStockDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioStockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        portfolio_id = self.kwargs['portfolio_id']
        return PortfolioStock.objects.filter(portfolio_id=portfolio_id)