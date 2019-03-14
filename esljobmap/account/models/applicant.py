# account/models/applicant.py

from django.db import models
from .user import SiteUser
from .resume import Resume
from .photo import Photo

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
                                default='',
                                null=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True, null=True, default=None)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True, null=True, default=None)

    @property
    def has_resume(self) -> bool:
        return self.resume is not None

    @property
    def has_photo(self) -> bool:
        return self.photo is not None

    @property
    def nice_visa_type(self) -> str:
        if self.visa_type is None:
            return 'VISA HOLDER'
        return self.visa_type.__str__()

    @property
    def nice_country(self) -> str:
        if self.country is None:
            return 'YOUR COUNTRY'
        return self.country.__str__()

    @property
    def status(self) -> str:
        return 'Banned' if self.user.is_banned else '-'
