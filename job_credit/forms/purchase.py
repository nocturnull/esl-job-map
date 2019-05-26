# job_credit/forms/purchase.py

from django import forms


class CreditPurchaseForm(forms.Form):
    single_credit = forms.IntegerField(label='1 credit set', min_value=0, max_value=1000, initial=0)
    ten_credits = forms.IntegerField(label='10 credits set', min_value=0, max_value=1000, initial=0)
    one_hundred_credits = forms.IntegerField(label='100 credits set', min_value=0, max_value=1000, initial=0)
