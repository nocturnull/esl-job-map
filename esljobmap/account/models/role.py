# account/models/role.py

from django.db import models
from .user import SiteUser

from ..apps import AccountConfig


class VisaType(models.Model):
    name = models.CharField(blank=False, max_length=255)

    class Meta:
        db_table = AccountConfig.name + '_visa_type'


class Country(models.Model):
    name = models.CharField(blank=False, max_length=255)
    code = models.CharField(blank=False, max_length=10)


class Teacher(models.Model):
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    visa_type = models.ForeignKey(VisaType,
                                  on_delete=models.CASCADE,
                                  verbose_name='The visa the person possesses',
                                  blank=True,
                                  null=True)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                verbose_name="The person's nationality",
                                blank=True,
                                null=True
                                )
