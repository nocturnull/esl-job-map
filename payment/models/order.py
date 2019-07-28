
from django.db import models

from account.models import SiteUser

from .plan import Plan


class Order(models.Model):
    """
    An order that is created for the users by admin so they can activate their subscription.
    """
    site_user = models.ForeignKey(SiteUser, on_delete=models.DO_NOTHING, related_name='order_customer')
    plan = models.OneToOneField(Plan, on_delete=models.DO_NOTHING, related_name='order')
    code = models.CharField(max_length=8)
    apply_trial = models.BooleanField(default=False)
    was_consumed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
