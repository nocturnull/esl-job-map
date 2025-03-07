
from django.db import models

from datetime import datetime, timedelta

from .product import Product

from nlib.formatter import currency_to_symbol


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
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='plan')
    amount = models.IntegerField()
    interval = models.CharField(max_length=32, choices=INTERVAL_CHOICES, default=INTERVAL_MONTH)
    currency = models.CharField(max_length=4, default='USD')
    trial_period_days = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calc_billing_date_after_trial(self) -> str:
        """
        Calculate and format billing date and format it.

        :return:
        """
        now = datetime.now() + timedelta(days=self.trial_period_days)
        return now.strftime('%b %d %Y')

    @property
    def billing_date_after_trial(self) -> datetime:
        """
        Get the actual date object for the billing date after the trial ends.

        :return:
        """
        return datetime.now() + timedelta(days=self.trial_period_days)

    @property
    def detailed_display(self) -> str:
        """
        Nice price display.

        :return:
        """
        return '{0}{1} per {2}'.format(self.amount, self.currency, self.interval)

    @property
    def trial_display(self) -> str:
        """
        Neatly format trial display.

        :return:
        """
        days = self.trial_period_days
        # Lazy solution
        if days == 7:
            return 'First week free'
        else:
            return 'First {} days free'.format(days)

    @property
    def billing_amount(self):
        """
        Label override.

        :return:
        """
        return self.amount

    @property
    def billing_interval(self):
        """
        Label override.

        :return:
        """
        return self.interval

    @property
    def symbol_currency(self) -> str:
        """
        Get the symbol version of the currency code.

        :return:
        """
        return currency_to_symbol(self.currency)

    @property
    def formatted_billing_amount(self) -> str:
        """
        Billing amount nicely displayed.

        :return:
        """
        return '{}{}'.format(self.symbol_currency, self.billing_amount)

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.product.name, self.billing_interval, self.trial_period_days)
