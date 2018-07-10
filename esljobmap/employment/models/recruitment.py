from django.db import models

from ..apps import EmploymentConfig


class JobPost(models.Model):
    title = models.CharField(max_length=512)
    class_type = models.CharField('The type of class the teaching job entails', max_length=255)
    location = models.CharField(max_length=512)
    contact_name = models.CharField(max_length=512)
    contact_email = models.EmailField(max_length=255)
    contact_number = models.CharField(max_length=255)
    schedule = models.CharField(max_length=512)
    other_requirements = models.TextField()
    is_full_time = models.BooleanField(default=False)

    class Meta:
        db_table = EmploymentConfig.name + '_job_post'
