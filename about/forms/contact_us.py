
from django import forms


class ContactUsForm(forms.Form):
    subject = forms.CharField(max_length=256)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
