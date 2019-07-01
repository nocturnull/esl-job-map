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
    def fifty_credits(self):
        """
        100 credits bundle count.

        :return:
        """
        return 50 * self.purchase_form.cleaned_data.get('fifty_credits')

    def get_credits(self) -> int:
        """
        Sum up the job credits.

        :return:
        """
        return self.single_credits + self.ten_credits + self.fifty_credits

    def calculate_total(self) -> int:
        """
        Calculates the total amount in cents.

        :return:
        """
        price_1 = STANDARD_PRICE * self.single_credits
        price_10 = DISCOUNTED_PRICE_1 * self.ten_credits
        price_50 = DISCOUNTED_PRICE_2 * self.fifty_credits
        return 100 * (price_1 + price_10 + price_50)
