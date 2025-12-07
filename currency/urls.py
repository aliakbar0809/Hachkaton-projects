from django.urls import path
from .views import DailyCurrencyRatesView

urlpatterns = [
    path("convertator/", DailyCurrencyRatesView.as_view(), name="daily_currency_rates"),
]
