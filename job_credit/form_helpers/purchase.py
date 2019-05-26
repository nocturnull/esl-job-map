# job_credit/form_helpers/purchase.py

from ..forms.purchase import CreditPurchaseForm

from ..settings import *


class PurchaseHelper:
    """Helper class for the credit purchase form."""

    def __init__(self, purchase_form: CreditPurchaseForm):
        """
        Constructor.

        :param purchase_form:
        """
        self.purchase_form = purchase_form

    @property
    def single_credits(self):
        """
        Single credit bundle count.

        :return:
        """
        return self.purchase_form.cleaned_data.get('single_credit')

    @property
    def ten_credits(self):
        """
        10 credits bundle count.

        :return:
        """
        return 10 * self.purchase_form.cleaned_data.get('ten_credits')

    @property
    def one_hundred_credits(self):
        """
        100 credits bundle count.

        :return:
        """
        return 100 * self.purchase_form.cleaned_data.get('one_hundred_credits')

    def get_credits(self) -> int:
        """
        Sum up the job credits.

        :return:
        """
        return self.single_credits + self.ten_credits + self.one_hundred_credits

    def calculate_total(self) -> int:
        """
        Calculates the total amount in cents.

        :return:
        """
        price_1 = HALF_PRICE * self.single_credits
        price_10 = HALF_PRICE * self.ten_credits
        price_100 = HALF_PRICE * self.one_hundred_credits
        return 100 * (price_1 + price_10 + price_100)
