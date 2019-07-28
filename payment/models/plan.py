
from django.db import models

from .product import Product


class Plan(models.Model):
    """
    Plans used for subscriptions.

    https://stripe.com/docs/api/plans/create
    """
    INTERVAL_DAY = 'day'
    INTERVAL_WEEK = 'week'
    INTERVAL_MONTH = 'month'
    INTERVAL_YEAR = 'year'
    INTERVAL_CHOICES = (
        (INTERVAL_DAY, INTERVAL_DAY),
        (INTERVAL_WEEK, INTERVAL_WEEK),
        (INTERVAL_MONTH, INTERVAL_MONTH),
        (INTERVAL_YEAR, INTERVAL_YEAR),
    )

    stripe_plan_id = models.CharField(max_length=32)
    product = models.OneToOneField(Product, on_delete=models.DO_NOTHING, related_name='plan')
    amount = models.IntegerField()
    interval = models.CharField(max_length=32, choices=INTERVAL_CHOICES, default=INTERVAL_MONTH)
    currency = models.CharField(max_length=4, default='USD')
    trial_period_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.amount, self.interval, self.currency)
