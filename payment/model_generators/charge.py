# payment/model_generators/charge.py

from account.models.user import SiteUser

from ..models.charge import Charge


class ChargeGenerator:

    @classmethod
    def create(cls, user: SiteUser, charge_id: str):
        """
        Create a charge.

        :param user:
        :param charge_id:
        :return:
        """
        Charge.objects.create(site_user=user, stripe_charge_id=charge_id, status=Charge.STATUS_COMPLETED)
