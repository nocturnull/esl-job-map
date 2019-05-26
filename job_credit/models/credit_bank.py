# job_credit/models/credit_bank.py

from django.db import models

from account.models import SiteUser


class Bank(models.Model):
    site_user = models.OneToOneField(SiteUser, on_delete=models.CASCADE, related_name='credit_bank')
    balance = models.FloatField(blank=True, default=0)
    updated_at = models.DateTimeField(auto_now=True)
