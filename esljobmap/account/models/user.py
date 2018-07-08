# account/models/user.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from ..managers import SiteUserManager
from ..apps import AccountConfig


class SiteUser(AbstractBaseUser, PermissionsMixin):
    """
    Extension of the default user.
    """
    USER_ROLES = (
        (1, 'nil'),
        (2, 'recruiter'),
        (3, 'teacher')
    )
    email = models.EmailField(unique=True, blank=False, max_length=255)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(blank=True, max_length=255, verbose_name='Contact phone number')
    role = models.PositiveSmallIntegerField(choices=USER_ROLES, default=1)

    is_staff = models.BooleanField(
        'Staff Status',
        default=False,
        help_text='Is the user an administrator'
    )
    is_active = models.BooleanField(
        'Active',
        default=True,
        help_text='Is the user account active'
    )
    USERNAME_FIELD = 'email'
    objects = SiteUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = AccountConfig.name + '_site_user'
