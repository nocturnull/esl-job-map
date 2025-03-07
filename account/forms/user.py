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
        fields = ('name', 'phone_number', 'opted_out_of_emails')


class AdminLoginForm(forms.Form):
    email = forms.EmailField(label='Account Email')

    class Meta:
        fields = ('email',)
