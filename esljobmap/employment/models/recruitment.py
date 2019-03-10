# employment/models/recruitment.py

from django.utils.html import escape
from django.urls import reverse
from datetime import datetime
from django.db import models

from esljobmap.model_attributes.localize import Localize

from ..apps import EmploymentConfig
from ..settings import *

from account.models.user import SiteUser


class JobPost(models.Model, Localize):
    """Model for a job post made by recruiters."""
    site_user = models.ForeignKey(SiteUser, related_name='job_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    class_type = models.CharField(max_length=255)
    schedule = models.CharField(max_length=512)
    other_requirements = models.CharField(max_length=1024, blank=True, default='')
    is_full_time = models.BooleanField('Job type', default=False)
    pay_rate = models.CharField(max_length=512, blank=True, default='')
    salary = models.CharField(max_length=512, blank=True, default='')
    benefits = models.CharField(max_length=1024, blank=True, default='')
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reposted_at = models.DateTimeField(blank=True, default=None, null=True)
    created_at_override = models.DateTimeField(blank=True, default=None, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=1024, default='')
    expiry_notice_sent = models.BooleanField(default=False, blank=True)

    _applicants = []

    @property
    def site_user_email(self) -> str:
        """
        Gets the users email.

        :return:
        """
        return self.site_user.email

    @property
    def recruiter_name(self) -> str:
        """
        Gets the users name.

        :return:
        """
        return self.site_user.name

    @property
    def recruiter_phone_number(self) -> str:
        """
        Gets the users phone number.

        :return:
        """
        return self.site_user.phone_number

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
    def days_valid_after_repost(self) -> int:
        """
        The amount of days the job is valid for changes when the job is reposted.

        :return:
        """
        if self.is_full_time:
            return REPOSTED_FULL_TIME_JOB_DAYS_VALID
        return REPOSTED_PART_TIME_JOB_DAYS_VALID

    @property
    def expires_in(self) -> int:
        """
        Determine how many days are left until the job expires.

        :return:
        """
        if self.reposted_at is None:
            return self.days_valid - (datetime.now() - self.created_at).days
        else:
            return self.days_valid_after_repost - (datetime.now() - self.reposted_at).days

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
    def is_taken_down(self) -> bool:
        """
        Determine if the jobs was taken down.

        :return:
        """
        return not self.is_visible

    @property
    def is_recruiter_banned(self) -> bool:
        """
        Determine if the related recruiter is banned.

        :return:
        """
        return self.site_user.is_banned

    @property
    def isvisible(self) -> bool:
        """
        Combination of different factors that can make a job hidden.

        :return:
        """
        return self.is_visible and not self.is_expired and not self.is_recruiter_banned

    @property
    def job_type(self) -> str:
        """
        Nice job type display.

        :return:
        """
        return 'Full' if self.is_full_time else 'Part'

    @property
    def was_reposted(self) -> bool:
        """
        Determine if the job was reposted.

        :return:
        """
        return True if self.reposted_at is not None else False

    @property
    def pretty_status(self) -> str:
        """
        Display the amount of days until the job expires in a neat format.

        :return:
        """
        if self.is_visible and not self.is_expired:
            days = (datetime.today() - self.reference_date).days
            return 'Posted {0} day(s) ago'.format(days)
        return 'Job closed'

    @property
    def pretty_days_elapsed(self) -> str:
        days = (datetime.today() - self.reference_date).days
        return 'Posted: {0} day(s) ago'.format(days)

    @property
    def reference_date(self) -> datetime:
        return self.created_at if self.reposted_at is None else self.reposted_at

    @property
    def edit_link(self):
        if self.is_full_time:
            return reverse('employment_edit_full_time_job_post', args=[self.id])
        return reverse('employment_edit_part_time_job_post', args=[self.id])

    @property
    def close_link(self):
        return reverse('employment_close_job_post', args=[self.id])

    @property
    def restore_link(self):
        return reverse('employment_restore_post', args=[self.id])

    @property
    def repost_link(self):
        return reverse('employment_repost_job_post', args=[self.id])

    @property
    def applicants_link(self):
        return reverse('employment_job_applicants', args=[self.id])

    @property
    def recruiter_create_job_link(self):
        if self.is_full_time:
            return reverse('employment_full_time_map') + '#postAnchor'
        return reverse('employment_part_time_map') + '#postAnchor'

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

    @property
    def applicant_count(self) -> int:
        """
        Ignores banned users.

        :return:
        """
        return self.applicants.count()

    def num_applicants(self, user) -> int:
        """
        Filter out any banned users from the count if needed.

        :param user:
        :return:
        """
        if user.is_authenticated and user.is_banned:
            count = self.applicants.count()
        else:
            count = 0
            for a in self.applicants.all():
                if a.site_user is not None:
                    if not a.site_user.is_banned:
                        count += 1
                else:
                    count += 1
        return count

    def pretty_num_applicants(self, user) -> str:
        """
        Prettify number of applicants.

        :param user:
        :return:
        """
        return str(self.num_applicants(user)) + ' applicant(s)'

    def build_html_content(self, user, request) -> str:
        """
        Build the map HTML content for ths Job Post.

        :param user:
        :param request:
        :return:
        """
        not_interested = self.not_interested(user)
        can_apply = self.can_apply(user)
        has_applied, application = self.has_applicant_applied(user)
        container_class = 'job-not-interested' if not_interested else ''
        desc_class = 'mobile' if request.user_agent.is_mobile else ''

        content = '<div class="job-post {}" id="jobPostCard">'.format(container_class)  # Open job-post
        if not not_interested:
            content += '<div class="job-description {}">'.format(desc_class)  # Open job-description
            content += '<span class="bold-text">' + escape(self.title) + '</span><br>'
            if self.is_full_time:
                content += '<span class="bold-text">Salary: </span>' + self.salary + '<br>'
            else:
                content += '<span class="bold-text">Pay Rate: </span>' + self.pay_rate + '<br>'
            content += '<span class="bold-text">Schedule: </span>' + self.schedule + '<br>'
            content += '<span class="bold-text">Class Type: </span>' + self.class_type + '<br>'

            if self.is_full_time:
                content += '<span class="bold-text">Benefits: </span>' + self.benefits + '<br>'

            content += '<span class="bold-text">Other Requirements: </span>' + self.other_requirements + '<br>'

            content += '</div>'  # Close job-description
            content += '<div>' + self.pretty_num_applicants(user) + ', ' + self.pretty_days_elapsed + '</div>'

        if can_apply:
            content += '<div class="action-links">'  # Open action-links

            if not not_interested and not has_applied:
                content += '<a href="' + reverse('employment_apply_to_job', args=(self.id,)) + \
                           '" class="job-apply-link action-link">Apply</a>'
                if user.is_authenticated:
                    content += '<a href="' + reverse('employment_track_job_disinterest', args=(self.id,)) + \
                               '" class="job-not-interested-link" onclick="return updateMapMarker(event, this, ' +\
                               str(self.id) + ', 1);">Hide Info</a>'
            content += '</div>'  # Close action-links

        elif user.is_recruiter and self.is_job_poster(user):
            content += '<div class="action-links">'  # Open action-links
            content += '<a href="{}" class="job-apply-link action-link">Edit job</a>'.format(self.edit_link)
            content += '<a href="{}" class="job-not-interested-link">Close</a>'.format(self.close_link)
            content += '</div>'  # Close action-links

        content += '</div>'  # Close job-post
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
        Determine if the user marked the current job post as not interesting.

        :param user:
        :return:
        """
        if user.is_authenticated:
            # Recruiters cannot mark a job post is not interesting.
            if not user.is_recruiter and user.disinterested_jobs is not None:
                for disinterested_job_post in user.disinterested_jobs:
                    if self == disinterested_job_post.job_post:
                        return True
        return False

    def __str__(self):
        return '%s %s' % (self.title, self.pretty_employment_type)

    class Meta:
        db_table = EmploymentConfig.name + '_job_post'
