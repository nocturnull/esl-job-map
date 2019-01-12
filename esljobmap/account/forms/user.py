# account/forms/user.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from ..models import SiteUser


class SiteUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ('email',)


class SiteUserChangeForm(UserChangeForm):

    class Meta:
        model = SiteUser
        fields = UserChangeForm.Meta.fields


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'phone_number')
