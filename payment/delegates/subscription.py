# payment/delegates/subscription.py

import stripe
from datetime import datetime
from typing import Optional

from account.models import SiteUser

from ..models import Subscription, Order, Customer
from ..settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class SubscriptionDelegate:
    """Subscription model delegate"""

    @staticmethod
    def create(user: SiteUser, order: Order, customer: Customer) -> Subscription:
        """
        Subscribe the user to the plan specified in the order.

        https://stripe.com/docs/api/subscriptions/create#create_subscription-trial_period_days
        :param user:
        :param order:
        :param customer:
        :return:
        """
        kwargs = {
            'customer': customer.stripe_customer_id,
            'items': [{
                'plan': order.plan.stripe_plan_id
            }]
        }
        if order.apply_trial:
            kwargs['trial_period_days'] = order.plan.trial_period_days

        # Create Stripe subscription.
        stripe_subscription = stripe.Subscription.create(**kwargs)

        # Create local subscription.
        return Subscription.objects.create(
            stripe_subscription_id=stripe_subscription.id,
            site_user=user,
            order=order,
            trial_from_plan=order.apply_trial,
            is_active=True
        )

    @staticmethod
    def get_bill_date(user: SiteUser) -> Optional[datetime]:
        """
        Try to lookup a subscription.

        https://stripe.com/docs/api/subscriptions/object#subscription_object-billing_cycle_anchor
        :param user:
        :return:
        """
        try:
            if user.has_subscription:
                # Used cached version to prevent more API calls.
                if user.next_billing_date is not None:
                    return user.next_billing_date

                # Attempt to lookup and set next billing date.
                subscription = user.active_subscription
                stripe_sub = stripe.Subscription.retrieve(subscription.stripe_subscription_id)
                user.next_billing_date = datetime.fromtimestamp(stripe_sub.billing_cycle_anchor)

                return user.next_billing_date
        except:
            return None
