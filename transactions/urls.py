from django.urls import path
from .views import TransactionCreateView
from .views import CombinedReportView

urlpatterns = [
    path("transactions/", TransactionCreateView.as_view(), name="create_transaction"),
    path("transactions/list/", CombinedReportView.as_view(), name="income_expense_list"),
]
