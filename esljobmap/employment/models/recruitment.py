# employment/models/recruitment.py

from datetime import datetime, timedelta
from django.db import models
from django.shortcuts import reverse

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
        """
        Display the employment information in neatly formatted text.

        :return: str
        """
        if self.is_full_time:
            return '[Full-Time]'
        return '[Part-Time]'

    @property
    def is_editable(self) -> bool:
        """
        Determine if the user can edit this Job Post.

        :return: bool
        """
        return datetime.now() < (self.created_at + timedelta(days=1))

    @property
    def is_expired(self) -> bool:
        """
        Determine if the Job Post has expired.

        :return: bool
        """
        return datetime.now() > (self.created_at + timedelta(weeks=2))

    @property
    def pretty_days_till_expired(self) -> str:
        """
        Display the amount of days until the job expires in a neat format.

        :return:
        """
        days_left = 14 - (datetime.now() - self.created_at).days
        if days_left > 0:
            return 'Expires in: {0} days'.format(days_left)
        return 'Expired'

    @property
    def html_content(self):
        """
        Build the map HTML content for ths Job Post.

        :return:
        """
        content = 'Title: ' + self.title + '<br>'
        if self.is_full_time:
            content += 'Salary: ' + self.salary + '<br>'
        else:
            content += 'Pay Rate: ' + self.pay_rate + '<br>'
        content += 'Schedule: ' + self.schedule + '<br>'
        content += 'Class Type: ' + self.class_type + '<br>'

        if self.is_full_time:
            content += 'Benefits: ' + self.benefits + '<br>'

        content += 'Other Requirements: ' + self.other_requirements + '<br>'
        content += self.pretty_days_till_expired + '<br>'
        content += '<a href="' + reverse('employment_apply_to_job', args=(self.id,)) + '" target="_blank">Apply</a>'
        return content

    def has_applicant_applied(self, user) -> bool:
        """
        Determine if the supplied applicant has already applied to this Job Post.

        :param user:
        :return: bool
        """
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
    created_at = models.DateTimeField(auto_now_add=True)
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
