# account/forms/applicant.py

from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms

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
    resume_file = forms.FileField(allow_empty_file=True, required=False, label='Resume')
    photo_file = forms.FileField(allow_empty_file=True, required=False, label='Photo')

    def __init__(self, *args, **kwargs):
        super(ApplicantUpdateForm, self).__init__(*args, **kwargs)
        self.fields['can_transfer_visa'].required = False
        self.fields['can_work_second_job'].required = False

    class Meta:
        model = Teacher
        fields = ('country', 'visa_type', 'can_transfer_visa',
                  'can_work_second_job', 'resume_file', 'photo_file')
