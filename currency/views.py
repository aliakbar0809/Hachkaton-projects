# currency/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response

class DailyCurrencyRatesView(APIView):
    def get(self, request):
        base = "tjs"
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            rates = data.get(base)
            if not rates:
                return Response({"error": "Нет курсов для базовой валюты", "raw": data}, status=500)

            filtered = {k.upper(): rates[k] for k in ["usd","eur","rub","tjs"] if k in rates}

            return Response({
                "base": base.upper(),
                "date": data.get("date"),
                "rates": filtered
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
