# account/models/role.py

from django.db import models
from .user import SiteUser

from cloud.storage import build_storage_url
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
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                verbose_name="Nationality",
                                blank=True,
                                null=True
                                )
    resume_filename = models.CharField(max_length=512, default='', verbose_name='Resume', blank=True, null=True)

    @property
    def resume_storage_path(self) -> str:
        return 'resume/{0}'.format(self.resume_filename)

    @property
    def resume_url(self) -> str:
        return build_storage_url(self.resume_storage_path)

    @property
    def has_resume(self) -> bool:
        return len(self.resume_filename) > 0
