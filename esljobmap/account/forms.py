# account/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SiteUser, Teacher
from django.db import transaction
from django.forms import ModelForm


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


class UserUpdateForm(ModelForm):

    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')


class TeacherUpdateForm(ModelForm):

    class Meta:
        model = Teacher
        fields = ('country', 'visa_type')
