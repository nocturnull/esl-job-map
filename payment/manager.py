# payment/manager.py

from django.db import transaction

from job_credit.model_generators.history import RecordGenerator
from account.models.user import SiteUser

from .delegates.subscription import SubscriptionDelegate
from .delegates.customer import CustomerDelegate
from .delegates.charge import ChargeDelegate
from .delegates.order import OrderDelegate

import stripe
from .settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class PaymentManager:
    """Payment flow manager"""

    @staticmethod
    def charge(job_credits: int, total_price: int, user: SiteUser, stripe_token: str) -> bool:
        """
        Create the stripe charge.

        :param job_credits:
        :param total_price:
        :param user:
        :param stripe_token:
        :return:
        """
        email = user.email
        d = '{} credit(s) purchase for {}'.format(job_credits, email)
        # Authorize and place purchase.
        try:
            charge = stripe.Charge.create(
                amount=total_price,
                currency='usd',
                source=stripe_token,
                description=d,
                receipt_email=email,
                metadata={
                    'email': email
                }
            )
        except Exception as e:
            print(e)
            return False

        with transaction.atomic():
            # Update job credit balance.
            user.credit_bank.balance += job_credits
            user.credit_bank.save()

            # Create stripe charge record.
            ChargeDelegate.create(user, charge.id)

            # Create credit history purchase record.
            RecordGenerator.track_purchase_record(user, job_credits)

        return True

    @staticmethod
    def subscribe(order_code: str, user: SiteUser, stripe_token: str) -> bool:
        """
        Attempt to subscribe the user to a plan.

        :param order_code:
        :param user:
        :param stripe_token:
        :return:
        """
        order = OrderDelegate.lookup(user, order_code)
        if order is not None:
            with transaction.atomic():
                customer = CustomerDelegate.get_or_create_customer(user, stripe_token)
                subscription = SubscriptionDelegate.create(user, order, customer)
                if subscription:
                    return True

        return False
