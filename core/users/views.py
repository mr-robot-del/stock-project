from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from stocks.serializers import StockSerializer
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from stocks.models import Stock
from .models import User
from .serializers import WatchlistAddSerializer
from rest_framework.generics import DestroyAPIView
User = get_user_model()

class UserListView(generics.ListAPIView):
    """
    API view to list all users (for admins or testing).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class RegisterView(generics.CreateAPIView):
    """View for user registration."""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """View for user login."""
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
        
class WatchlistView(generics.ListCreateAPIView):
    """View user's watchlist (GET: list, POST: add stock by ID)."""
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WatchlistAddSerializer
        return StockSerializer

    def get_queryset(self):
        return self.request.user.watchlist.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock_id = serializer.validated_data['stock_id']

        try:
            stock = Stock.objects.get(id=stock_id)
            request.user.watchlist.add(stock)
            return Response(StockSerializer(stock).data, status=status.HTTP_201_CREATED)
        except Stock.DoesNotExist:
            return Response({'error': 'Stock not found'}, status=status.HTTP_404_NOT_FOUND)
        
class WatchlistRemoveView(DestroyAPIView):
    """Remove a stock from user's watchlist by ID."""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        stock_id = self.kwargs['stock_id']
        try:
            stock = Stock.objects.get(id=stock_id)
            if stock not in self.request.user.watchlist.all():
                raise Stock.DoesNotExist  # 404 if not in watchlist
            return stock
        except Stock.DoesNotExist:
            raise Stock.DoesNotExist

    def delete(self, request, *args, **kwargs):
        stock = self.get_object()
        request.user.watchlist.remove(stock)
        return Response(status=status.HTTP_204_NO_CONTENT)