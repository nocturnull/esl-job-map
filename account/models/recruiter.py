
from django.db import models

from ..models import SiteUser

from ..apps import AccountConfig


class AutofillOptions(models.Model):
    site_user = models.OneToOneField(SiteUser, related_name='autofill_options', on_delete=models.CASCADE)
    ft_class_type = models.CharField('Class type', blank=True, max_length=255)
    ft_other_requirements = models.CharField('Other requirements', max_length=1024, blank=True, default='')
    ft_salary = models.CharField('Salary', max_length=512, blank=True, default='')
    ft_benefits = models.CharField('Benefits', max_length=1024, blank=True, default='')
    pt_class_type = models.CharField('Class type', blank=True, max_length=255)
    pt_schedule = models.CharField('Schedule', blank=True, max_length=512)
    pt_pay_rate = models.CharField('Pay rate', max_length=512, blank=True, default='')
    pt_other_requirements = models.CharField('Other requirements', max_length=1024, blank=True, default='')

    class Meta:
        db_table = AccountConfig.name + '_autofill_options'
