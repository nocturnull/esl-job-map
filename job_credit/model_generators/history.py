# job_credit/model_generators/history.py

from django.core.exceptions import MultipleObjectsReturned

from account.settings import JOB_CREDIT_POST_EXPENSE
from account.models.user import SiteUser

from ..models.history import Record

from typing import Optional
from datetime import datetime


class RecordGenerator:
    """Job Credit Record generator"""

    @classmethod
    def track_post_record(cls, user: SiteUser, is_full_time: bool):
        """
        Create a new record for a job credits transaction.
        If one exists for today already then update that instead.

        :param user:
        :param is_full_time:
        :return:
        """
        action = Record.ACTION_CONSUME
        existing_record = cls._get_existing_daily_record(user, action)
        if existing_record is None:
            description = cls._generate_new_description(is_full_time)
            Record.objects.create(
                site_user=user, description=description, action=action,
                amount=JOB_CREDIT_POST_EXPENSE, balance=user.credits)
        else:
            existing_record.amount += 1
            existing_record.description = cls._regenerate_description(existing_record)
            existing_record.balance = user.credits
            existing_record.save()

    @classmethod
    def track_purchase_record(cls, user: SiteUser, job_credits: int):
        """
        Create a new record for purchasing.

        :param user:
        :param job_credits:
        :return:
        """
        action = Record.ACTION_PURCHASE
        existing_record = cls._get_existing_daily_record(user, action)
        if existing_record is None:
            Record.objects.create(
                site_user=user, description='Purchased {} credit(s)'.format(job_credits), action=action,
                amount=job_credits, balance=user.credits)
        else:
            existing_record.amount += job_credits
            existing_record.balance = user.credits
            existing_record.description = 'Purchased {} credit(s)'.format(existing_record.amount)
            existing_record.save()

    @classmethod
    def track_refund_record(cls, user: SiteUser, job_credits: float):
        """
        Create a or updated a record for refunds.

        :param user:
        :param job_credits:
        :return:
        """
        action = Record.ACTION_REFUND
        existing_record = cls._get_existing_daily_record(user, action)
        if existing_record is None:
            Record.objects.create(
                site_user=user, description='Refunded {:.1f} credit(s)'.format(job_credits), action=action,
                amount=job_credits, balance=user.credits
            )
        else:
            existing_record.amount += job_credits
            existing_record.balance = user.credits
            existing_record.description = 'Refunded {:.1f} credit(s)'.format(existing_record.amount)
            existing_record.save()

    @classmethod
    def _get_existing_daily_record(cls, user: SiteUser, action: str) -> Optional[Record]:
        """
        Search for an existing record for the current day.

        :param user:
        :param action:
        :return:
        """
        local_date = datetime.now().date()
        kwargs = dict(site_user=user, created_at__date=local_date, action=action)
        rec = None

        try:
            rec = Record.objects.get(**kwargs)
        except MultipleObjectsReturned:
            rec = Record.objects.filter(**kwargs).latest('created_at')
        except Record.DoesNotExist:
            pass
        return rec

    @classmethod
    def _generate_new_description(cls, is_full_time: bool) -> str:
        """
        Dynamically generator the appropriate description of the record.

        :param is_full_time:
        :return:
        """
        if is_full_time:
            return 'Posted a full-time job'
        return 'Posted a part-time job'

    @classmethod
    def _regenerate_description(cls, record: Record) -> str:
        return 'Posted {} Jobs'.format(record.amount)
