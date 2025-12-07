from django.urls import path
from .views import TransactionCreateView
from .views import IncomeReportView, ExpenseReportView

urlpatterns = [
    path('upload/', TransactionCreateView.as_view(), name='transactions-upload'),
    path("income/", IncomeReportView.as_view(), name="income_report"),
    path("expense/", ExpenseReportView.as_view(), name="expense_report"),
]
