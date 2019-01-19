# employment/models/recruitment.py

from django.shortcuts import reverse
from datetime import datetime
from django.db import models

from ..settings import FULL_TIME_JOB_DAYS_VALID, PART_TIME_JOB_DAYS_VALID
from ..model_attributes.localize import Localize
from ..apps import EmploymentConfig

from account.models.user import SiteUser


class JobPost(models.Model, Localize):
    """Model for a job post made by recruiters."""
    site_user = models.ForeignKey(SiteUser, related_name='job_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    class_type = models.CharField(max_length=255)
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

    _applicants = []

    @property
    def days_valid(self) -> int:
        """
        Get how many days the job is valid for.

        :return: int
        """
        if self.is_full_time:
            return FULL_TIME_JOB_DAYS_VALID
        return PART_TIME_JOB_DAYS_VALID

    @property
    def expires_in(self) -> int:
        """
        Determine how many days are left until the job expires.

        :return:
        """
        return self.days_valid - (datetime.now() - self.created_at).days

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
    def is_expired(self) -> bool:
        """
        Determine if the Job Post has expired.

        :return: bool
        """
        return self.expires_in < 1

    @property
    def pretty_status(self) -> str:
        """
        Display the amount of days until the job expires in a neat format.

        :return:
        """
        if self.is_visible and not self.is_expired:
            days = (datetime.today() - self.created_at).days
            return 'Posted {0} day(s) ago'.format(days)
        return 'Job closed'

    @property
    def pretty_days_elapsed(self) -> str:
        days = (datetime.today() - self.created_at).days
        return 'Posted: {0} day(s) ago'.format(days)

    @property
    def pretty_num_applicants(self) -> str:
        return str(self.applicants.count()) + ' applicant(s)'

    @property
    def edit_link(self):
        if self.is_full_time:
            return reverse('employment_edit_full_time_job_post', args=[self.id])
        return reverse('employment_edit_part_time_job_post', args=[self.id])

    @property
    def card_class(self) -> str :
        if self.is_full_time:
            return 'full-time'
        return 'part-time'

    @property
    def tags(self) -> str:
        tags = 'all'

        # Job type
        if self.is_full_time:
            tags += ',full-time'
        else:
            tags += ',part-time'

        # Status
        if self.is_expired or not self.is_visible:
            tags += ',closed'
        else:
            tags += ',active'

        return tags

    def build_html_content(self, user) -> str:
        """
        Build the map HTML content for ths Job Post.

        :return: str
        """
        not_interested = self.not_interested(user)
        can_apply = self.can_apply(user)
        has_applied, application = self.has_applicant_applied(user)
        container_class = ''

        if not_interested:
            container_class = 'job-not-interested'

        content = '<div class="job-post" id="jobPostCard">'
        content += '<div class="job-description ' + container_class + '">'
        content += '<span class="bold-text">' + self.title + '</span><br>'
        if self.is_full_time:
            content += '<span class="bold-text">Salary: </span>' + self.salary + '<br>'
        else:
            content += '<span class="bold-text">Pay Rate: </span>' + self.pay_rate + '<br>'
        content += '<span class="bold-text">Schedule: </span>' + self.schedule + '<br>'
        content += '<span class="bold-text">Class Type: </span>' + self.class_type + '<br>'

        if self.is_full_time:
            content += '<span class="bold-text">Benefits: </span>' + self.benefits + '<br>'

        content += '<span class="bold-text">Other Requirements: </span>' + self.other_requirements + '<br>'

        content += '</div>'
        content += self.pretty_num_applicants + ', ' + self.pretty_days_elapsed + '<br>'

        if can_apply:
            content += '<div class="action-links">'

            if not_interested:
                content += '<a href="#" class="job-apply-link disabled">Apply</a>'
                content += '<a href="' + reverse('employment_remove_job_disinterest', args=(self.id,)) + \
                           '" class="action-link" onclick="return updateMapMarker(event, this, ' +\
                           str(self.id) + ', 0);">Interested</a>'
            elif not has_applied:
                content += '<a href="' + reverse('employment_apply_to_job', args=(self.id,)) + \
                           '" class="job-apply-link action-link">Apply</a>'
                if user.is_authenticated:
                    content += '<a href="' + reverse('employment_track_job_disinterest', args=(self.id,)) + \
                               '" class="job-not-interested-link" onclick="return updateMapMarker(event, this, ' +\
                               str(self.id) + ', 1);">Not Interested</a>'
                else:
                    content += '<a href="#" class="job-not-interested-link" ' \
                               'data-open="noticeModal">Not Interested</a>'
            content += '</div><br>'

        content += '</div>'
        if has_applied:
            content += '<span class="bold-text">Applied: </span>' + application.nice_created_at + '<br>'

        return content

    def has_applicant_applied(self, user) -> tuple:
        """
        Determine if the supplied applicant has already applied to this Job Post.

        :param user:
        :return: tuple
        """
        applied = False
        application = None

        if user.is_authenticated:
            # Only check applicants.
            if not user.is_recruiter:
                if len(self._applicants) == 0:
                    self._applicants = self.applicants.all()

                for a in self._applicants:
                    if user == a.site_user:
                        applied = True
                        application = a
                        break

        return applied, application

    def is_job_poster(self, user) -> bool:
        """
        Determine if the supplied user is the original poster.

        :param user:
        :return:
        """
        if user.is_authenticated:
            return self.site_user == user
        return False

    def can_apply(self, user) -> bool:
        """
        Determine if the user can apply.

        :param user:
        :return:
        """
        if user.is_authenticated:
            # Recruiters cannot apply to job posts.
            return not user.is_recruiter
        return True

    def not_interested(self, user) -> bool:
        """
        Determine if the user marked the current job post is not interesting.

        :param user:
        :return:
        """
        if user.is_authenticated:
            # Recruiters cannot mark a job post is not interesting.
            if not user.is_recruiter:
                for disinterested_job_post in user.disinterested_job_posts.all():
                    if self == disinterested_job_post.job_post:
                        return True
        return False

    def __str__(self):
        return '%s %s' % (self.title, self.pretty_employment_type)

    class Meta:
        db_table = EmploymentConfig.name + '_job_post'
