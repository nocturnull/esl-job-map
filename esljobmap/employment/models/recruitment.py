from django.db import models

from ..apps import EmploymentConfig
from account.models.user import SiteUser


class JobPost(models.Model):
    site_user = models.ForeignKey(SiteUser, related_name='job_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    class_type = models.CharField(max_length=255)
    location = models.CharField(max_length=512)
    contact_name = models.CharField(max_length=512)
    contact_email = models.EmailField(max_length=255)
    contact_number = models.CharField(max_length=255)
    schedule = models.CharField(max_length=512)
    other_requirements = models.CharField(max_length=1024, blank=True, default='')
    is_full_time = models.BooleanField(default=False)
    pay_rate = models.PositiveIntegerField(blank=True, default=0, help_text='** ,000 won per hour')
    salary = models.PositiveIntegerField(verbose_name='Yearly Salary', blank=True, default=0)
    benefits = models.CharField(max_length=1024, blank=True, default='')

    @property
    def pretty_employment_type(self):
        if self.is_full_time:
            return '[Full Time]'
        return '[Part Time]'

    def __str__(self):
        return '%s %s' % (self.title, self.pretty_employment_type)

    class Meta:
        db_table = EmploymentConfig.name + '_job_post'
