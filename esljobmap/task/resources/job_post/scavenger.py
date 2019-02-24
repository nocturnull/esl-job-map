# task/resources/job_post/scavenger.py

from datetime import datetime, timedelta

from employment.models import JobPost
from employment.settings import *


class JobPostScavenger:
    """Job Post database scavenger"""

    @classmethod
    def get_expired_full_time(cls):
        """
        Search for all expired full time jobs.

        :return:
        """
        exp_date = datetime.now() - timedelta(days=FULL_TIME_JOB_DAYS_VALID)
        queryset = JobPost.objects\
            .filter(is_full_time=True, expiry_notice_sent=False, created_at__lte=exp_date)\
            .prefetch_related('site_user')

        return cls._filter_reposted_jobs(queryset)

    @classmethod
    def get_expired_part_time(cls):
        """
        Search for all expired part time jobs.

        :return:
        """
        exp_date = datetime.now() - timedelta(days=PART_TIME_JOB_DAYS_VALID)
        queryset = JobPost.objects\
            .filter(is_full_time=False, expiry_notice_sent=False, created_at__lte=exp_date)\
            .prefetch_related('site_user')

        return cls._filter_reposted_jobs(queryset)

    @classmethod
    def _filter_reposted_jobs(cls, jobs):
        """
        Ensure the job has expired, reposted jobs have a seperate date to check.

        :param jobs:
        :return:
        """
        return [j for j in jobs if j.is_expired]
