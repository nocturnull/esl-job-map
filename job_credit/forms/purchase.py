# job_credit/forms/purchase.py

from django import forms


class CreditPurchaseForm(forms.Form):
    single_credit = forms.IntegerField(label='1 credit set', min_value=0, max_value=1000, initial=0)
    ten_credits = forms.IntegerField(label='10 credit set', min_value=0, max_value=1000, initial=0)
    fifty_credits = forms.IntegerField(label='50 credit set', min_value=0, max_value=1000, initial=0)
    order_code = forms.CharField(label='Custom Order Code',
                                 max_length=8,
                                 required=False,
                                 widget=forms.TextInput(attrs={'class': 'order-code'}))
