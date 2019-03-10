# account/admin.py

from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.contrib import admin

from .forms.user import SiteUserCreationForm, SiteUserChangeForm
from .models import SiteUser, Teacher


class SiteUserAdmin(UserAdmin):
    add_form = SiteUserCreationForm
    form = SiteUserChangeForm
    model = SiteUser
    list_display = ['email', 'local_date_joined', 'full_name', 'role']
    ordering = ('-date_joined',)
    search_fields = ('email',)
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('email', 'password', 'name', 'first_name', 'last_name', 'phone_number')}),
        ('Preferences', {'fields': ('opted_out_of_emails',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'is_banned')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


def resume_link(obj):
    if obj.has_resume:
        return mark_safe('<a href={} target="_blank">View</a>'.format(obj.resume.cdn_url))
    return ''


def photo_link(obj):
    if obj.has_photo:
        return mark_safe('<a href={} target="_blank">View</a>'.format(obj.photo.cdn_url))
    return ''


class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'join_date', 'visa_type', 'country', resume_link, photo_link]

    def join_date(self, obj):
        return obj.user.local_date_joined

    join_date.admin_order_field = 'user__date_joined'


admin.site.site_header = 'ESL Job Map Admin Site'
admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
