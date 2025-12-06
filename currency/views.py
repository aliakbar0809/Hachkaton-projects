# currency/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CurrencySerializer

API_KEY = "ba3520efa48cddcdecbd28dc2ccf62df755891fa"
API_URL = "https://api.bankfxapi.com/v1/bank/TNB"

class CurrencyRatesAPIView(APIView):
    def get(self, request):
        base_currency = request.query_params.get("base", "USD")
        target_currency = request.query_params.get("target")

        headers = {
            "x-api-key": API_KEY
        }

        params = {
            "base": base_currency
        }

        try:
            response = requests.get(API_URL, headers=headers, params=params)
            data = response.json()

            # Ошибка API
            if response.status_code != 200:
                return Response(data, status=response.status_code)

            # Если пользователь хочет конкретную валюту
            if target_currency:
                rate = data["data"]["sell"].get(target_currency.upper())
                if rate is None:
                    return Response({"error": "Валюта не найдена"}, status=status.HTTP_404_NOT_FOUND)
                return Response({target_currency.upper(): rate})

            # Если нужны все курсы
            serializer = CurrencySerializer(data=data)
            serializer.is_valid()
            return Response(data)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
