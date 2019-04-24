# job_credit/model_generators/history.py

from account.settings import JOB_CREDIT_POST_EXPENSE
from account.models.user import SiteUser

from ..models.history import Record


class RecordOriginator:
    """Job Credit Record generator"""

    @classmethod
    def create_post_record(cls, user: SiteUser, is_consumption: bool, is_full_time: bool):
        """
        Create a new record for a job credits transaction.

        :param user:
        :param is_consumption:
        :param is_full_time:
        :return:
        """
        action = Record.ACTION_CONSUME if is_consumption else Record.ACTION_PURCHASE
        description = cls._generator_description(is_full_time)
        Record.objects.create(site_user=user, description=description, action=action,
                              amount=JOB_CREDIT_POST_EXPENSE, balance=user.job_credits)

    @classmethod
    def _generator_description(cls, is_full_time: bool) -> str:
        """
        Dynamically generator the appropriate description of the record.

        :param is_full_time:
        :return:
        """
        if is_full_time:
            return 'Posted a full-time job'
        return 'Posted a part-time job'
