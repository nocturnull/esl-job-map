
from django import forms

from ..models import Plan

import stripe
from ..settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class CreatePlanForm(forms.ModelForm):
    trial_period_days = forms.IntegerField(label='Free days at Start', min_value=0)
    amount = forms.IntegerField(label='Billing Amount', min_value=1)
    interval = forms.ChoiceField(label='Billing Interval', choices=Plan.INTERVAL_CHOICES)

    def save(self, commit=True):
        stripe_plan = stripe.Plan.create(
            amount=self.instance.amount * 100,
            interval=self.instance.interval,
            product=self.instance.product.stripe_product_id,
            currency=self.instance.currency
        )
        
        self.instance.stripe_plan_id = stripe_plan.id
        return super(CreatePlanForm, self).save(commit=commit)

    class Meta:
        model = Plan
        fields = ['product', 'amount', 'interval', 'currency', 'trial_period_days']
