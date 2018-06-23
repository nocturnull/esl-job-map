# account/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class SiteUser(AbstractUser):
    USER_ROLES = (
        (1, 'nil'),
        (2, 'recruiter'),
        (3, 'teacher')
    )
    email = models.EmailField(blank=False, max_length=255, help_text='Required. Provide a valid email address.')
    phone_number = models.CharField(blank=True, max_length=255, verbose_name='Contact phone number')
    role = models.PositiveSmallIntegerField(choices=USER_ROLES, default=1)

    def __str__(self):
        return self.email


class VisaType(models.Model):
    name = models.CharField(blank=False, max_length=255)


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
