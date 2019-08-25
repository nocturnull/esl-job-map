# account/models/user.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from datetime import datetime, timedelta

from esljobmap.model_attributes.localize import Localize
from employment.settings import JOB_DAYS_VALID

from ..managers import SiteUserManager
from ..apps import AccountConfig


class SiteUser(AbstractBaseUser, PermissionsMixin, Localize):
    """
    Extension of the default user.
    """
    ROLE_NIL = 1
    ROLE_RECRUITER = 2
    ROLE_TEACHER = 3

    USER_ROLES = (
        (1, 'nil'),
        (2, 'recruiter'),
        (3, 'teacher')
    )
    email = models.EmailField(unique=True, blank=False, max_length=255)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, verbose_name='Name', default='')
    first_name = models.CharField(max_length=255, blank=True, verbose_name='First Name', default='')
    last_name = models.CharField(max_length=255, blank=True, verbose_name='Last Name', default='')
    phone_number = models.CharField(blank=True, max_length=255, verbose_name='Contact Number')
    role = models.PositiveSmallIntegerField(choices=USER_ROLES, default=1)
    opted_out_of_emails = models.BooleanField('Don’t receive copy of application emails', default=False, blank=True)
    is_banned = models.BooleanField(default=False, blank=True)
    opted_out_of_expired_job_emails = models.BooleanField('Don’t receive job expire notification emails', default=False, blank=True)

    _disinterested_jobs = None
    _has_subscription = None
    _subscription = None

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

    @property
    def is_teacher(self) -> bool:
        """
        Determine if the user is an applicant.

        :return:
        """
        return self.role == self.ROLE_TEACHER

    @property
    def is_recruiter(self) -> bool:
        """
        Determine if the user is a recruiter.

        :return:
        """
        return self.role == self.ROLE_NIL or self.role == self.ROLE_RECRUITER

    @property
    def disinterested_jobs(self):
        """
        Cache disinterested jobs in a local variable to prevent multiple db hits.

        :return:
        """
        if self._disinterested_jobs is None:
            self._disinterested_jobs = self.disinterested_job_posts.all()
        return self._disinterested_jobs

    @property
    def credits(self) -> float:
        """
        Format job credits when needed.

        :return:
        """
        try:
            if self.credit_bank.balance > 0:
                return self.credit_bank.balance
            return int(self.credit_bank.balance)
        except ObjectDoesNotExist:
            if self.is_recruiter:
                from job_credit.models.credit_bank import Bank
                Bank.objects.create(site_user=self)
            return 0

    @property
    def has_credits(self) -> bool:
        """
        Determine if the user has credits.

        :return:
        """
        if self.is_recruiter and self.credits > 0:
            return True
        return False

    @property
    def autofill(self):
        """
        Safely get autofill options.

        :return:
        """
        try:
            return self.autofill_options
        except:
            from ..models.recruiter import AutofillOptions
            return AutofillOptions()

    @property
    def has_subscription(self) -> bool:
        """
        Determine if the user has an active subscription.

        :return:
        """
        if self.is_recruiter:
            if self._has_subscription is None:
                try:
                    self._subscription = self.customer_subscriptions.get(is_active=True)
                    self._has_subscription = True
                except:
                    self._has_subscription = False
            return self._has_subscription
        return False

    @property
    def active_jobs(self):
        """
        Get the currently active jobs.

        :return:
        """
        expire_date = datetime.today() - timedelta(days=JOB_DAYS_VALID)
        return self.job_posts.filter(is_visible=True, posted_at__gte=expire_date)

    @property
    def active_job_count(self) -> int:
        """
        Get the amount of currently active jobs.

        :return:
        """
        return self.active_jobs.count()

    def __str__(self):
        return self.email

    class Meta:
        db_table = AccountConfig.name + '_site_user'
