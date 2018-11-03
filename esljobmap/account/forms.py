# account/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SiteUser, Teacher
from django.db import transaction


class SiteUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ('email',)


class SiteUserTeacherCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ('email',)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 3
        user.save()
        Teacher.objects.create(user=user)
        return user


class SiteUserRecruiterCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 2
        user.save()
        return user


class SiteUserChangeForm(UserChangeForm):

    class Meta:
        model = SiteUser
        fields = UserChangeForm.Meta.fields


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'phone_number')


class TeacherUpdateForm(forms.ModelForm):
    resume_filename = forms.FileField(allow_empty_file=True, required=False, label='Resume')

    def __init__(self, *args, **kwargs):
        super(TeacherUpdateForm, self).__init__(*args, **kwargs)
        self.fields['can_transfer_visa'].required = False
        self.fields['can_work_second_job'].required = False

    class Meta:
        model = Teacher
        fields = ('country', 'visa_type', 'can_transfer_visa', 'can_work_second_job', 'resume_filename')
