
from datetime import datetime, timedelta
import random

from ..models import JobPost
from ..settings import *


class PostManager:
    @staticmethod
    def has_existing_location(job_post: JobPost) -> bool:
        """
        Determine if there is already a job with the exact same location.

        :param job_post:
        :return:
        """
        days_diff = 30 if job_post.is_full_time else 15
        expired_date = datetime.now() - timedelta(days=days_diff)

        return JobPost.objects.filter(is_visible=True,
                                      created_at__gt=expired_date,
                                      address__exact=job_post.address).count() > 0

    @staticmethod
    def offset_location(job_post: JobPost):
        lat_mag = -1 if random.random() < 0.5 else 1
        lng_mag = -1 if random.random() < 0.5 else 1
        job_post.latitude += (lat_mag * LAT_OFFSET * random.random() * 3)
        job_post.longitude += (lng_mag * LNG_OFFSET * random.random() * 3)
