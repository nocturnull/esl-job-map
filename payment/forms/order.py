
from django import forms

from ..models import Order
from nlib.ran import random_string


class CreateOrderForm(forms.ModelForm):
    
    def save(self, commit=True):
        self.instance.code = random_string()
        return super(CreateOrderForm, self).save(commit=commit)

    class Meta:
        model = Order
        fields = ['site_user', 'plan', 'apply_trial']
