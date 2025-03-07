
from django.db import models

from account.models import SiteUser


class Customer(models.Model):
    """
    Customers are used to make recurring charges.

    https://stripe.com/docs/api/customers
    """
    site_user = models.OneToOneField(SiteUser, on_delete=models.DO_NOTHING, related_name='payment_customer')
    stripe_customer_id = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}-{1}'.format(self.site_user, self.stripe_customer_id)
