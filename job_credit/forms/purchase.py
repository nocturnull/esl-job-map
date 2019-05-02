# job_credit/forms/purchase.py

from django import forms


class CreditPurchaseForm(forms.Form):
    credits = forms.IntegerField(label='Credits', min_value=1, max_value=1000, initial=1)
