
from django.db import models


class Record(models.Model):
    ACTION_PURCHASE = 'purchase'
    ACTION_CONSUME = 'consume'
    ACTION_CHOICES = (
        (ACTION_PURCHASE, 'Purchased'),
        (ACTION_CONSUME, 'Consumed')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=128, choices=ACTION_CHOICES, default=ACTION_CONSUME)
    amount = models.FloatField(default=0)
    balance = models.FloatField(default=0)
