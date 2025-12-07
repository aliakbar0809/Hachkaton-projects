from django.urls import path
from .views import DailyCurrencyRatesView

urlpatterns = [
    path('convert/', DailyCurrencyRatesView.as_view(), name='currency-convert'),
]
