from django.urls import path
from .views import RegisterView, LoginView
from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
]