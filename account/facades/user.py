# account/facades/user.py

from ..models import SiteUser
from ..settings import *


class UserFacade:
    """User related business logic facade"""

    def __init__(self, user: SiteUser):
        """
        Constructor

        :param user:
        """
        self.instance = user

    def has_active_subscription(self) -> bool:
        """
        Determine if the user has an active subscription.

        :return:
        """
        return self.instance.has_subscription

    def can_afford_post(self) -> bool:
        """
        Determine if the user is allowed to post

        :return:
        """
        return self.instance.credits >= JOB_CREDIT_POST_EXPENSE

    def consume_post_credits(self):
        """
        Consumes N credits for posting a new job.

        :return:
        """
        self.instance.credit_bank.balance -= JOB_CREDIT_POST_EXPENSE
        self.instance.credit_bank.save()

    def has_reached_post_limit(self) -> bool:
        """
        Determine if the recruiter has reached the post limit.

        :return:
        """
        return self.instance.active_jobs >= MAX_JOBS
