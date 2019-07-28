
from django.db import models


class Product(models.Model):
    """
    Product used for orders or subscriptions.

    https://stripe.com/docs/api/service_products/create
    """
    stripe_product_id = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    descriptor = models.CharField(max_length=22, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
