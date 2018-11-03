
from django.db import models

from ..apps import EmploymentConfig
from account.models.user import SiteUser
from .recruitment import JobPost


class DisinterestedJobPost(models.Model):
    site_user = models.ForeignKey(SiteUser, related_name='disinterested_job_posts', on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)

    class Meta:
        db_table = EmploymentConfig.name + '_disinterested_job_post'
