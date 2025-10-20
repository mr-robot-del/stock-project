"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.schemas import get_schema_view

# Temporary root view
def home(request):
    return HttpResponse("Welcome to Stock Project API")

# Temporary favicon view
def favicon(request):
    return HttpResponse(status=204)

schema_view = get_schema_view(
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', home, name='home'),
    path('favicon.ico', favicon),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/docs/', schema_view, name='api-docs'),
    path('users/', include('users.urls')),
    path('stocks/', include('stocks.urls')),
    path('alerts/', include('alerts.urls')),
    path('analysis/', include('analysis.urls')),
    path('portfolios/', include('portfolios.urls')),
    
]