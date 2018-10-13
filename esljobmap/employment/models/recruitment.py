# employment/models/recruitment.py

from datetime import datetime, timedelta
from django.db import models

from ..apps import EmploymentConfig
from account.models.user import SiteUser
from account.models.resume import Resume


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
    is_full_time = models.BooleanField('Job type', default=False)
    pay_rate = models.CharField(max_length=512, blank=True, default='')
    salary = models.CharField(max_length=512, blank=True, default='')
    benefits = models.CharField(max_length=1024, blank=True, default='')
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=1024, default='')

    @property
    def pretty_employment_type(self) -> str:
        if self.is_full_time:
            return '[Full-Time]'
        return '[Part-Time]'

    @property
    def is_editable(self) -> bool:
        return datetime.now() < (self.created_at + timedelta(days=1))

    @property
    def is_expired(self) -> bool:
        return datetime.now() > (self.created_at + timedelta(weeks=2))

    @property
    def pretty_days_till_expired(self) -> str:
        days_left = 14 - (datetime.now() - self.created_at).days
        if days_left > 0:
            return 'Expires in: {0} days'.format(days_left)
        return 'Expired'

    def has_applicant_applied(self, user) -> bool:
        if user.is_authenticated:
            job_applications = self.applicants.all()
            if len(job_applications) > 0:
                applicants = map(lambda j: j.site_user, job_applications)
                return user in applicants
        return False

    def __str__(self):
        return '%s %s' % (self.title, self.pretty_employment_type)

    class Meta:
        db_table = EmploymentConfig.name + '_job_post'


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
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=False)

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
