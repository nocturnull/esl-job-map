# payment/manager.py

from django.db import transaction

from job_credit.model_generators.history import RecordGenerator
from account.models.user import SiteUser

from .model_generators.charge import ChargeGenerator

import stripe

stripe.api_key = 'sk_test_TzT4TCtBdG3u6yhx7tbCUpFZ00NQFlq0re'


class PaymentManager:
    """Payment flow manager"""

    @staticmethod
    def charge(job_credits: int, total_price: int, user: SiteUser, stripe_token: str):
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

        with transaction.atomic():
            # Update job credit balance.
            user.credit_bank.balance += job_credits
            user.credit_bank.save()

            # Create stripe charge record.
            ChargeGenerator.create(user, charge.id)

            # Create credit history purchase record.
            RecordGenerator.track_purchase_record(user, job_credits)
