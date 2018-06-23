from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SiteUserCreationForm, SiteUserChangeForm
from .models import SiteUser


class SiteUserAdmin(UserAdmin):
    add_form = SiteUserCreationForm
    form = SiteUserChangeForm
    model = SiteUser
    list_display = ['email', 'username']


admin.site.register(SiteUser, SiteUserAdmin)
