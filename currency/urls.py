# currency/urls.py
from django.urls import path
from .views import CurrencyRatesAPIView

urlpatterns = [
    path('rates/', CurrencyRatesAPIView.as_view(), name='currency-rates'),
]
