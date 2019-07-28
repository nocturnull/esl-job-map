
from django import forms

from ..models import Product

import stripe
from ..settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


class CreateProductForm(forms.ModelForm):

    def save(self, commit=True):
        kwargs = {
            'name': self.instance.name,
            'type': 'service'
        }
        if self.instance.descriptor:
            kwargs['statement_descriptor'] = self.instance.descriptor

        stripe_product = stripe.Product.create(**kwargs)
        self.instance.stripe_product_id = stripe_product.id
        return super(CreateProductForm, self).save(commit=commit)

    class Meta:
        model = Product
        fields = ['name', 'descriptor']
