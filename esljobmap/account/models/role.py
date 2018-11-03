# account/models/role.py

from django.db import models
from .user import SiteUser
from .resume import Resume

from ..apps import AccountConfig


class VisaType(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = AccountConfig.name + '_visa_type'


class Country(models.Model):
    name = models.CharField(blank=False, max_length=255, verbose_name='Nationality')
    code = models.CharField(blank=False, max_length=10)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    visa_type = models.ForeignKey(VisaType,
                                  on_delete=models.CASCADE,
                                  verbose_name='Visa Status',
                                  blank=True,
                                  null=True)
    can_transfer_visa = models.BooleanField(verbose_name='My visa can be transferred to new employer',
                                            default=False,
                                            blank=True)
    can_work_second_job = models.BooleanField(verbose_name='My current employer has given permission to work a second job',
                                              default=False,
                                              blank=True)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                verbose_name="Nationality",
                                blank=True,
                                null=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def has_resume(self) -> bool:
        return self.resume is not None

    @property
    def is_e1e2_holder(self) -> bool:
        return self.visa_type.id == 2
