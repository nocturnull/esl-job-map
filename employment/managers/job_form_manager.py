
from ..forms.job_post.create import CreateFullTimeJobForm, CreatePartTimeJobForm

from account.models import SiteUser


class JobFormManager:
    """Manager for full time and part time job forms"""

    @staticmethod
    def filled_full_time_form(user: SiteUser):
        """
        Fills in the full time form with the recruiters preferred options.

        :param user:
        :return:
        """
        autofill = user.autofill
        return CreateFullTimeJobForm(initial={
            'class_type': autofill.class_type,
            'schedule': autofill.schedule,
            'other_requirements': autofill.other_requirements,
            'salary': autofill.salary,
            'benefits': autofill.benefits
        })

    @staticmethod
    def filled_part_time_form(user: SiteUser):
        """
        Fills in the part time form with the recruiters preferred options.

        :param user:
        :return:
        """
        autofill = user.autofill
        return CreatePartTimeJobForm(initial={
            'class_type': autofill.class_type,
            'schedule': autofill.schedule,
            'other_requirements': autofill.other_requirements,
            'pay_rate': autofill.pay_rate
        })
