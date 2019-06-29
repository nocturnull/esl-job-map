
from django.db import models

from ..models import SiteUser

from ..apps import AccountConfig


class AutofillOptions(models.Model):
    site_user = models.OneToOneField(SiteUser, related_name='autofill_options', on_delete=models.CASCADE)
    class_type = models.CharField(max_length=255)
    schedule = models.CharField(max_length=512)
    other_requirements = models.CharField(max_length=1024, blank=True, default='')
    pay_rate = models.CharField(max_length=512, blank=True, default='')
    salary = models.CharField(max_length=512, blank=True, default='')
    benefits = models.CharField(max_length=1024, blank=True, default='')

    class Meta:
        db_table = AccountConfig.name + '_autofill_options'
