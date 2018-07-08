from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import SiteUserCreationForm, SiteUserChangeForm
from .models import SiteUser


class SiteUserAdmin(UserAdmin):
    add_form = SiteUserCreationForm
    form = SiteUserChangeForm
    model = SiteUser
    list_display = ['email', 'first_name', 'last_name', 'date_joined']
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.site_header = 'ESL Job Map Admin Site'
admin.site.register(SiteUser, SiteUserAdmin)
