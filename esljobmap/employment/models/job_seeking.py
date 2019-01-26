# employment/models/job_seeking.py

from django.urls import reverse_lazy
from django.db import models

from account.models import Resume, Photo, SiteUser

from esljobmap.model_attributes.localize import Localize

from ..models.recruitment import JobPost
from ..apps import EmploymentConfig


class JobApplication(models.Model, Localize):
    """Model for job applications made by applicants."""
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
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True, null=True, default=None)
    cover_letter = models.TextField(default='')

    @property
    def tags(self):
        tags = 'all'
        if self.job_post.is_visible and not self.job_post.is_expired:
            tags += ',open'
        else:
            tags += ',expired'

        return tags

    @property
    def nice_created_at(self) -> str:
        return self.created_at.strftime('%x')

    @property
    def has_photo(self) -> bool:
        return self.photo is not None

    @property
    def view_url(self) -> str:
        return reverse_lazy('employment_view_application', args=[self.id])

    @classmethod
    def create_application(cls, **kwargs):
        return cls.objects.create(**kwargs)

    def __str__(self):
        return self.job_post.__str__()

    class Meta:
        db_table = EmploymentConfig.name + '_job_application'
