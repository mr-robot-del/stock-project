from django.contrib.auth.models import AbstractUser
from django.db import models
from stocks.models import Stock
class User(AbstractUser):
    email = models.EmailField(unique=True)
    joined = models.DateTimeField(auto_now_add=True)
    
    watchlist = models.ManyToManyField(Stock, blank=True, related_name='watchers')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    