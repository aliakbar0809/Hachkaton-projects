import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DailyCurrencyRatesView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'base',
                openapi.IN_QUERY,
                description="Базовая валюта (tjs, usd, eur, rub)",
                type=openapi.TYPE_STRING,
                required=False,
                default="tjs"
            ),
            openapi.Parameter(
                'amount',
                openapi.IN_QUERY,
                description="Сумма в базовой валюте",
                type=openapi.TYPE_NUMBER,
                required=False,
                default=1
            ),
        ],
        responses={200: "OK"}
    )
    def get(self, request):
      
        base = request.GET.get("base", "tjs").lower()
        amount = float(request.GET.get("amount", 1))

        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            rates = data.get(base)
            if not rates:
                return Response({"error": "Нет курсов для базовой валюты", "raw": data}, status=500)

           
            target_currencies = ["tjs", "usd", "eur", "rub"]

          
            converted = {}
            for k in target_currencies:
                if k in rates:
                    converted[k.upper()] = round(amount * rates[k], 2)

            return Response({
                "base": base.upper(),
                "amount": amount,
                "date": data.get("date"),
                "converted": converted
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)


# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .predictor import predict_7_days_from_current
from rest_framework.views import APIView

class Predict7DaysAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['currency', 'type', 'current_rate'],
            properties={
                'currency': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Валюта (USD, EUR, RUB)',
                    example='USD'
                ),
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Тип курса ('buy' или 'sell')",
                    example='sell'
                ),
                'current_rate': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Текущий курс для прогнозирования',
                    example=9.3275
                ),
            }
        ),
        responses={200: "OK"}
    )
    def post(self, request):
        currency = request.data.get("currency", "USD").upper()
        rate_type = request.data.get("type", "sell").lower()
        current_rate = request.data.get("current_rate")

        if current_rate is None or not isinstance(current_rate, (int, float)):
            return Response({"error": "current_rate обязателен и должен быть числом"}, status=400)

        if currency not in ["USD", "EUR", "RUB"]:
            return Response({"error": "Валюта должна быть USD, EUR или RUB"}, status=400)
        if rate_type not in ["buy", "sell"]:
            return Response({"error": "type должен быть 'buy' или 'sell'"}, status=400)

        try:
            result = predict_7_days_from_current(
                current_rate=current_rate,
                currency=currency,
                rate_type=rate_type
            )
            return Response(result, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
