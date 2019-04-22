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
    amount = models.FloatField(default=0)
    balance = models.FloatField(default=0)

    def generate_description(self):
        """
        TODO
        :return:
        """
        self.description = ''

    def __str__(self):
        return 'site_user={}, action={}, amount={}'.format(self.site_user, self.action, self.amount)
