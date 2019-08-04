
import stripe

from account.models import SiteUser

from ..models import Customer
from ..settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class CustomerDelegate:
    """Customer modal delegate"""

    @staticmethod
    def get_or_create_customer(user: SiteUser, stripe_token: str) -> Customer:
        """
        Get an existing Stripe customer or create a new one both locally and on stripe.

        :param user:
        :param stripe_token:
        :return:
        """
        try:
            return user.payment_customer
        except Exception as e:
            print(e)
        # Create on stripe.
        stripe_customer = stripe.Customer.create(email=user.email, source=stripe_token)
        # Track on our database.
        customer = Customer.objects.create(site_user=user, stripe_customer_id=stripe_customer.id)
        return customer

