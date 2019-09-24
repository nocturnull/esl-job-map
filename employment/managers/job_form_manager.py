
from ..forms.job_post.create import CreateFullTimeJobForm, CreatePartTimeJobForm

from account.models import SiteUser, AutofillOptions


class JobFormManager:
    """Manager for full time and part time job forms"""

    @staticmethod
    def filled_full_time_form(user: SiteUser):
        """
        Fills in the full time form with the recruiters preferred options.

        :param user:
        :return:
        """
        try:
            autofill = user.autofill
        except AttributeError:
            autofill = AutofillOptions()

        return CreateFullTimeJobForm(initial={
            'class_type': autofill.ft_class_type,
            'other_requirements': autofill.ft_other_requirements,
            'salary': autofill.ft_salary,
            'benefits': autofill.ft_benefits
        })

    @staticmethod
    def filled_part_time_form(user: SiteUser):
        """
        Fills in the part time form with the recruiters preferred options.

        :param user:
        :return:
        """
        try:
            autofill = user.autofill
        except AttributeError:
            autofill = AutofillOptions()

        return CreatePartTimeJobForm(initial={
            'class_type': autofill.pt_class_type,
            'schedule': autofill.pt_schedule,
            'other_requirements': autofill.pt_other_requirements,
            'pay_rate': autofill.pt_pay_rate
        })
