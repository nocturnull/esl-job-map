
import stripe
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
            'customer': customer.id,
            'items': [{
                'plan': order.plan.stripe_plan_id
            }]
        }
        if order.apply_trial:
            kwargs['trial_period_days'] = order.plan.trial_period_days

        # Create Stripe subscription.
        stripe_subscription = stripe.Subscription.create(**kwargs)

        # Update the order to inform us that the user consumed the order code.
        order.was_consumed = True
        order.save()

        # Create local subscription.
        return Subscription.objects.create(
            stripe_subscription_id=stripe_subscription.id,
            site_user=user,
            order=order,
            trial_from_plan=order.apply_trial,
            is_active=True
        )
