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
