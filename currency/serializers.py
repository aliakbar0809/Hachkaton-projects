
from rest_framework import serializers

class CurrencySerializer(serializers.Serializer):
    base = serializers.CharField()
    rates = serializers.DictField()
