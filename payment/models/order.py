
from django.db import models

from account.models import SiteUser

from .plan import Plan


class Order(models.Model):
    """
    An order that is created for the users by admin so they can activate their subscription.
    """
    site_user = models.ForeignKey(SiteUser, on_delete=models.DO_NOTHING, related_name='order_customer')
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, related_name='order')
    code = models.CharField(max_length=8, unique=True)
    apply_trial = models.BooleanField(default=False)
    was_consumed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def detailed_info(self) -> str:
        """
        A summary of what the order entails.

        :return:
        """
        if self.apply_trial:
            return '{0}. {1}. First billing {2} for {3}'.format(
                self.plan.product.descriptor,
                self.plan.trial_display,
                self.plan.calc_billing_date_after_trial(),
                self.plan.formatted_billing_amount
            )
        else:
            return '{0} [{1}]'.format(self.plan.product.descriptor, self.plan.detailed_display)

    @property
    def price_info(self) -> str:
        """
        Price information when checking out.

        :return:
        """
        if self.apply_trial:
            return '{0} for {1}0'.format(
                self.plan.product.short_descriptor,
                self.plan.symbol_currency
            )

    def __str__(self):
        return '{0}-{1}'.format(self.site_user, self.code)
