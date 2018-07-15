from django.db import models

from ..apps import EmploymentConfig


class JobPost(models.Model):
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

    def __str__(self):
        return '%s' % self.title

    class Meta:
        db_table = EmploymentConfig.name + '_job_post'
