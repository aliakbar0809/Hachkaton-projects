import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DailyCurrencyRatesView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'amount',
                openapi.IN_QUERY,
                description="Сумма в TJS",
                type=openapi.TYPE_NUMBER,
                required=False
            ),
        ],
        responses={200: "OK"}
    )
    def get(self, request):
        amount = float(request.GET.get("amount", 1))

        base = "tjs"
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            rates = data.get(base)
            if not rates:
                return Response({"error": "Нет курсов для базовой валюты", "raw": data}, status=500)

            
            filtered = {}
            for k in ["usd", "eur", "rub", "tjs"]:
                if k in rates:
                    filtered[k.upper()] = round(amount * rates[k], 2)

            return Response({
                "base": base.upper(),
                "amount": amount,
                "date": data.get("date"),
                "converted": filtered
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
