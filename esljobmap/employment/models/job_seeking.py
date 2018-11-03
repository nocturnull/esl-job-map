
from django.db import models

from account.models.resume import Resume
from account.models.user import SiteUser

from ..apps import EmploymentConfig
from ..models.recruitment import JobPost


class JobApplication(models.Model):
    job_post = models.ForeignKey(JobPost,
                                 on_delete=models.CASCADE,
                                 related_name='applicants')
    site_user = models.ForeignKey(SiteUser,
                                  related_name='job_applications',
                                  on_delete=models.CASCADE,
                                  blank=True,
                                  null=True)
    contact_email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=False)

    @property
    def tags(self):
        tags = 'closed'
        if self.job_post.is_visible and not self.job_post.is_expired:
            tags = 'in-consideration'

        return tags

    @classmethod
    def create_application(cls, job_post, contact_email, resume, site_user=None):
        return cls.objects.create(job_post=job_post,
                                  contact_email=contact_email,
                                  resume=resume,
                                  site_user=site_user)

    def __str__(self):
        return self.job_post.__str__()

    class Meta:
        db_table = EmploymentConfig.name + '_job_application'
