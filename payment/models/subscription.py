# payment/models/subscription.py

from django.db import models

from account.models import SiteUser

from .order import Order


class Subscription(models.Model):
    """
    The actual subscription the customer paid for.

    https://stripe.com/docs/api/subscriptions
    """
    stripe_subscription_id = models.CharField(max_length=32)
    site_user = models.ForeignKey(SiteUser, on_delete=models.DO_NOTHING, related_name='customer_subscriptions')
    order = models.OneToOneField(Order, on_delete=models.DO_NOTHING, related_name='order_subscription')
    trial_from_plan = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def code_consumed(self):
        """
        Label override.

        :return:
        """
        return self.created_at

    def __str__(self):
        return '{0}-{1}'.format(self.site_user, self.stripe_subscription_id)
