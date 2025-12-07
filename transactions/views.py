
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



class IncomeReportView(ListAPIView):
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(type=Transaction.INCOME).order_by('-date')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('category_name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('amount_min', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('amount_max', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('date_after', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('date_before', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ExpenseReportView(ListAPIView):
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(type=Transaction.EXPENSE).order_by('-date')

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('category_name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('amount_min', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('amount_max', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
            openapi.Parameter('date_after', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('date_before', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)