# job_credit/models/history.py

from django.db import models

from account.models import SiteUser


class Record(models.Model):
    ACTION_PURCHASE = 'purchase'
    ACTION_CONSUME = 'consume'
    ACTION_CHOICES = (
        (ACTION_PURCHASE, 'Purchased'),
        (ACTION_CONSUME, 'Consumed')
    )

    site_user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name='credit_history')
    description = models.CharField(max_length=1024, default='', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=128, choices=ACTION_CHOICES, default=ACTION_CONSUME)
    amount = models.IntegerField(default=0)
    balance = models.FloatField(default=0)

    @property
    def is_purchase(self) -> bool:
        """
        Determine if the record is a purchase.

        :return:
        """
        return self.action == self.ACTION_PURCHASE

    @property
    def pretty_date(self) -> str:
        """
        Get a neatly formatted date.

        :return:
        """
        return self.created_at.strftime('%Y/%m/%d')

    @property
    def pretty_delta(self) -> str:
        """
        Get a neatly formatted delta factor.

        :return:
        """
        if self.is_purchase:
            return '+{}'.format(self.amount)
        return '-{}'.format(self.amount)

    def __str__(self):
        return 'site_user={}, action={}, amount={}'.format(self.site_user, self.action, self.amount)
