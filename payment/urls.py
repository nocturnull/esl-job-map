# payment/urls.py

from django.urls import path

from .views.order import OrderLookup


urlpatterns = [
    path('order/', OrderLookup.as_view(), name='order_lookup'),
    path('order/<str:code>', OrderLookup.as_view(), name='order_lookup_code')
]
