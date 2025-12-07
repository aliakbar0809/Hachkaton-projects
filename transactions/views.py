
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from .models import Transaction
from .serializers import TransactionSerializer
from .filter import TransactionFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Transaction
from .serializers import TransactionSerializer
from .filter import TransactionFilter


class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @swagger_auto_schema(request_body=TransactionSerializer(many=True))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)



class CombinedReportView(ListAPIView):
    serializer_class = TransactionSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter('category_name', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('amount_min', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter('amount_max', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter('date_after', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('date_before', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Всегда возвращаем все фильтры с пустыми значениями, если пользователь их не заполнил
        filters = {
            "category": request.query_params.get("category", None),
            "category_name": request.query_params.get("category_name", ""),
            "amount_min": request.query_params.get("amount_min", None),
            "amount_max": request.query_params.get("amount_max", None),
            "date_after": request.query_params.get("date_after", ""),
            "date_before": request.query_params.get("date_before", ""),
            "type": request.query_params.get("type", ""),
        }
        return Response({
            "filters": filters,
            "transactions": serializer.data
        })

    def get_queryset(self):
        queryset = Transaction.objects.all().order_by('-date')
        params = self.request.query_params

        if params.get('category'):
            queryset = queryset.filter(category_id=params['category'])
        if params.get('category_name'):
            queryset = queryset.filter(category__name__icontains=params['category_name'])
        if params.get('type') in [Transaction.INCOME, Transaction.EXPENSE]:
            queryset = queryset.filter(type=params['type'])
        if params.get('amount_min'):
            queryset = queryset.filter(amount__gte=float(params['amount_min']))
        if params.get('amount_max'):
            queryset = queryset.filter(amount__lte=float(params['amount_max']))
        if params.get('date_after'):
            queryset = queryset.filter(date__gte=params['date_after'])
        if params.get('date_before'):
            queryset = queryset.filter(date__lte=params['date_before'])

        return queryset