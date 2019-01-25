# account/forms/applicant.py

from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms

from esljobmap.validators import validate_pdf_extension, validate_jpeg_extension

from ..models import SiteUser, Teacher


class ApplicantCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text='Must be at least 8 characters',
    )

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ('email',)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 3
        user.email = user.email.lower()
        user.save()
        Teacher.objects.create(user=user)
        return user


class ApplicantUpdateForm(forms.ModelForm):
    resume_file = forms.FileField(allow_empty_file=True, required=False, label='Resume', validators=[validate_pdf_extension])
    photo_file = forms.FileField(allow_empty_file=True, required=False, label='Photo', validators=[validate_jpeg_extension])

    class Meta:
        model = Teacher
        fields = ('country', 'visa_type', 'resume_file', 'photo_file')
