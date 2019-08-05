
from django import forms

from ..models import Plan

import stripe
from ..settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class CreatePlanForm(forms.ModelForm):

    def save(self, commit=True):
        stripe_plan = stripe.Plan.create(
            amount=self.instance.amount,
            interval=self.instance.interval,
            product=self.instance.product.stripe_product_id,
            currency=self.instance.currency
        )
        
        self.instance.stripe_plan_id = stripe_plan.id
        return super(CreatePlanForm, self).save(commit=commit)

    class Meta:
        model = Plan
        fields = ['product', 'amount', 'interval', 'currency', 'trial_period_days']
