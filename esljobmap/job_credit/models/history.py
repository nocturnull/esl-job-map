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
    created_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=128, choices=ACTION_CHOICES, default=ACTION_CONSUME)
    amount = models.FloatField(default=0)
    balance = models.FloatField(default=0)
