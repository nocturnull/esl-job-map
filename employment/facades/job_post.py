# employment/facades/job_post.py

from account.models.user import SiteUser
from job_credit.model_generators.history import RecordGenerator


class JobPostFacade:
    """
    Facade for job credit and record related logic.
    """

    @staticmethod
    def refund_existing_jobs(user: SiteUser) -> int:
        """
        Attempt to refund existing jobs and also create a record for it.

        :param user:
        :return:
        """
        refund_credits = 0
        # Calculate refund amount for all active jobs.

        for job_post in user.active_jobs:
            refund_credits += job_post.calculate_refund()

        if refund_credits > 0:
            user.credit_bank.balance += refund_credits
            user.credit_bank.save()
            RecordGenerator.track_refund_record(user, job_credits=refund_credits)

        return refund_credits
