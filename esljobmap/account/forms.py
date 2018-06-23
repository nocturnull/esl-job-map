# account/forms.py
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import SiteUser


class SiteUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ('username', 'email')


class SiteUserChangeForm(UserChangeForm):

    class Meta:
        model = SiteUser
        fields = UserChangeForm.Meta.fields
