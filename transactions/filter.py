import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    amount_min = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    date_after = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_before = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    category_name = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Transaction
        fields = ['type', 'category']
