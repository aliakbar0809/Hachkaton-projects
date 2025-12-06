# bank_project/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bank API",
        default_version='v1',
        description="API для хакатона: транзакции, платежи, кредиты, валюты",
        contact=openapi.Contact(email="example@mail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Transactions — кейс 4
    path('transactions/', include('transactions.urls')),  

    # Currency — кейс 7
    path('currency/', include('currency.urls')),
]
