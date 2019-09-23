
from django import forms

from ..models import Product

import stripe
from ..settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class CreateProductForm(forms.ModelForm):
    name = forms.CharField(label='Internal Name', max_length=128)
    max_jobs = forms.IntegerField(label='Max Jobs', min_value=10)
    short_descriptor = forms.CharField(label='Name Displayed on Checkout', max_length=128)
    descriptor = forms.CharField(label='Name Displayed on Site',
                                 max_length=255,
                                 empty_value='',
                                 required=False)

    def save(self, commit=True):
        kwargs = {
            'name': self.instance.name,
            'type': 'service'
        }

        stripe_product = stripe.Product.create(**kwargs)
        self.instance.stripe_product_id = stripe_product.id
        return super(CreateProductForm, self).save(commit=commit)

    class Meta:
        model = Product
        fields = ['name', 'max_jobs', 'short_descriptor', 'descriptor']
