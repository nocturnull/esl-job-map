# employment/model_decorators/job_post.py

from datetime import datetime, timedelta
import random

from account.models import SiteUser

from ..models import JobPost
from ..settings import *


class ArrayedJobPost:
    """Model decorator for a JobPost"""

    def __init__(self, job_post: JobPost):
        """
        Constructor

        :param job_post:
        """
        self.instance = job_post

    @property
    def is_full_time(self) -> bool:
        """
        is_full_time inner property accessor.

        :return:
        """
        return self.instance.is_full_time

    def has_existing_location(self) -> bool:
        """
        Determine if there is already a job with the exact same location.

        :return: bool
        """
        cutoff_date = datetime.now() - timedelta(days=self.instance.days_valid)

        return JobPost.objects.filter(is_visible=True,
                                      created_at__gt=cutoff_date,
                                      address__exact=self.instance.address).count() > 0

    def normalize_location(self):
        """
        Attempts to normalize the location of the job if necessary.

        :return:
        """
        if self.has_existing_location():
            lat_mag = -1 if random.random() < 0.5 else 1
            lng_mag = -1 if random.random() < 0.5 else 1
            self.instance.latitude += (lat_mag * LAT_OFFSET * random.random() * 3)
            self.instance.longitude += (lng_mag * LNG_OFFSET * random.random() * 3)

    def create(self, is_full_time: bool, user: SiteUser, is_subscription: bool = False):
        """
        Create a new job post.

        :param is_full_time:
        :param user:
        :param is_subscription:
        :return:
        """
        self.instance.is_full_time = is_full_time
        self.instance.site_user = user
        self.instance.posted_at = datetime.now()
        self.instance.is_subscription_job = is_subscription
        self.instance.save()

    def repost(self, is_subscription: bool = False):
        """
        Set an existing job post as a repost.

        :return:
        """
        # Update current job
        self.instance.was_cloned = True
        self.instance.save()

        # Make clone of job that acts as repost
        self.instance.pk = None
        self.instance.reposted_at = datetime.now()
        self.instance.posted_at = self.instance.reposted_at
        self.instance.expiry_notice_sent = False
        self.instance.is_visible = True
        self.instance.is_subscription_job = is_subscription
        self.instance.save()
