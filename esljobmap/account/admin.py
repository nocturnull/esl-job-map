# account/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms.user import SiteUserCreationForm, SiteUserChangeForm
from .models import SiteUser, Teacher


class SiteUserAdmin(UserAdmin):
    add_form = SiteUserCreationForm
    form = SiteUserChangeForm
    model = SiteUser
    list_display = ['email', 'full_name', 'role', 'local_date_joined']
    ordering = ('email',)
    search_fields = ('email',)
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('email', 'password', 'name', 'first_name', 'last_name', 'contact_email', 'phone_number')}),
        ('Preferences', {'fields': ('opted_out_of_emails',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'visa_type', 'country', 'resume', 'photo']


admin.site.site_header = 'ESL Job Map Admin Site'
admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
