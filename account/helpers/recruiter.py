
from ..models import SiteUser


class RecruiterHelper:
    """Helper class for recruiter related tasks."""

    @staticmethod
    def opt_out_of_expired_post_emails(payload: dict) -> str:
        """
        Opt the recruiter out of email notifications when they request.

        :param payload:
        :return:
        """
        msg = 'Unable to complete the request. Either the link has expired or is invalid.'
        if payload is not None:
            try:
                usr = SiteUser.objects.get(email=payload['email'])
                usr.opted_out_of_expired_job_emails = True
                usr.save()
                msg = 'You have been opted out of emails!'
            except (KeyError, SiteUser.DoesNotExist):
                pass

        return msg
