# account/forms/applicant.py

from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms

from esljobmap.validators import validate_pdf_extension, validate_jpeg_extension

from ..models import SiteUser, Teacher, Country
from ..settings import *


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
    country = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        """
        Constructor

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.order_by('id').all()

    class Meta:
        model = Teacher
        fields = ('country', 'visa_type', 'resume_file', 'photo_file')

    @transaction.atomic
    def save(self, commit=True):
        """
        Save this form's self.instance object, ban the user if necessary.

        :param commit:
        :return:
        """
        applicant = super().save(commit=False)
        visa_type = applicant.visa_type_id
        country = applicant.country_id
        is_banned = applicant.user.is_banned
        if not is_banned:
            if visa_type is not None and country is not None:
                if visa_type not in ACCEPTED_VISAS and \
                        country not in ACCEPTED_COUNTRIES:
                    applicant.user.is_banned = True
                else:
                    applicant.user.is_banned = False
        applicant.user.save()
        applicant.save()
        return applicant
