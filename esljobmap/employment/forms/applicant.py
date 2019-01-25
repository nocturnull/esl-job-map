# employment/forms/applicant.py

from django import forms

from esljobmap.validators import validate_pdf_extension, validate_jpeg_extension


class ApplyToJobForm(forms.Form):
    """Form for applicants to apply to a job."""
    email_body = forms.CharField(widget=forms.Textarea(attrs={'rows': '18'}))
    resume = forms.FileField(allow_empty_file=True, required=False, validators=[validate_pdf_extension])
    photo = forms.FileField(allow_empty_file=True, required=False, validators=[validate_jpeg_extension])
    contact_email = forms.EmailField(label='Your email', max_length=255)
