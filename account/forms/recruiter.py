# account/forms/recruiter.py

from django.contrib.auth.forms import UserCreationForm
from django import forms

from ..models import SiteUser, AutofillOptions


class RecruiterCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text='Must be at least 8 characters',
    )

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 2
        user.email = user.email.lower()
        user.save()
        return user


class RecruiterUpdateForm(forms.ModelForm):

    class Meta:
        model = SiteUser
        fields = ('name', 'phone_number', 'opted_out_of_expired_job_emails', 'opted_out_of_emails')


class AutofillOptionsForm(forms.ModelForm):

    class Meta:
        model = AutofillOptions
        fields = ('ft_other_requirements', 'ft_salary', 'ft_benefits',
                  'pt_class_type', 'pt_schedule', 'pt_pay_rate', 'pt_other_requirements')
