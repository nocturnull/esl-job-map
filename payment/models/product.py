
from django.db import models


class Product(models.Model):
    """
    Product used for orders or subscriptions.

    https://stripe.com/docs/api/service_products/create
    """
    stripe_product_id = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    max_jobs = models.IntegerField(default=100)
    descriptor = models.CharField(max_length=255, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def internal_name(self):
        """
        Name label override.

        :return:
        """
        return self.name

    def __str__(self):
        return self.name
