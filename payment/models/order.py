
from django.db import models

from account.models import SiteUser

from .plan import Plan


class Order(models.Model):
    """
    An order that is created for the users by admin so they can activate their subscription.
    """
    site_user = models.ForeignKey(SiteUser, on_delete=models.DO_NOTHING, related_name='order_customer')
    plan = models.OneToOneField(Plan, on_delete=models.DO_NOTHING, related_name='order')
    code = models.CharField(max_length=8, unique=True)
    apply_trial = models.BooleanField(default=False)
    was_consumed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def summary(self) -> str:
        """
        A summary of what the order entails.

        :return:
        """
        return self.plan.product.descriptor

    def __str__(self):
        return '{0}-{1}'.format(self.site_user, self.code)
