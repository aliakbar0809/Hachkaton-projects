from django.urls import path
from .views import TransactionCreateView, TransactionReportView

urlpatterns = [
    path('upload/', TransactionCreateView.as_view(), name='transactions-upload'),
    path('report/', TransactionReportView.as_view(), name='transactions-report'),
]
