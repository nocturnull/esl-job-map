# account/model_regulators/user.py

from ..models import SiteUser
from ..settings import *


class UserTransformer:
    """User model data regulator"""

    def __init__(self, user: SiteUser):
        """
        Constructor

        :param user:
        """
        self.instance = user

    def can_afford_post(self) -> bool:
        """Determine if the user is allowed to post"""
        return self.instance.job_credits >= JOB_CREDIT_POST_EXPENSE

    def consume_post_credits(self):
        """
        Consumes N credits for posting a new job.

        :return:
        """
        self.instance.job_credits -= JOB_CREDIT_POST_EXPENSE
        self.instance.save()
