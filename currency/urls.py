
from django.urls import path
from . import views
from django.urls import path
from .views import DailyCurrencyRatesView, Predict7DaysAPIView

urlpatterns = [
    path('convert/', DailyCurrencyRatesView.as_view(), name='currency-convert'),
    path('predict/7days/', Predict7DaysAPIView.as_view(), name='predict_7days'),
    
]
