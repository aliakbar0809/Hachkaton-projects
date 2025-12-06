
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @swagger_auto_schema(request_body=TransactionSerializer(many=True))
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)




class TransactionReportView(APIView):
    def get(self, request):
        qs = Transaction.objects.all()

        total = qs.aggregate(Sum('amount'))['amount__sum'] or 0

        categories = qs.values('category__name').annotate(sum=Sum('amount'))

        report = [
            {
                'category': c['category__name'],
                'sum': c['sum'],
            }
            for c in categories
        ]

        return Response({
            'total': total,
            'categories': report
        })
