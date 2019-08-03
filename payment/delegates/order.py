
from typing import Optional

from account.models import SiteUser
from ..models import Order


class OrderDelegate:

    @staticmethod
    def lookup(user: SiteUser, code: str) -> Optional[Order]:
        """
        Determine if the code is associated with the user.

        :param user:
        :param code:
        :return:
        """
        try:
            o = Order.objects.get(site_user=user, code=code)
        except Order.DoesNotExist:
            o = None

        return o
