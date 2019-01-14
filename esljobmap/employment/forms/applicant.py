# employment/forms/applicant.py

from django import forms


class ApplyToJobForm(forms.Form):
    """Form for applicants to apply to a job."""
    email_body = forms.CharField(widget=forms.Textarea(attrs={'rows': '18'}))
    resume = forms.FileField(allow_empty_file=True, required=False)
    photo = forms.FileField(allow_empty_file=True, required=False)
    contact_email = forms.EmailField(label='Your email', max_length=255)
