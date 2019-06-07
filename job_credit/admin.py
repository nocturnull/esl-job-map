# job_credit/admin.py

from django.contrib import admin

from .forms.update import CreditRecordCreationForm
from .models.history import Record

from account.models.user import SiteUser


class CreditRecordAdmin(admin.ModelAdmin):
    list_display = ['site_user', 'local_created_at', 'action', 'amount', 'description']
    form = CreditRecordCreationForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'site_user':
            kwargs["queryset"] = SiteUser.objects.filter(role=SiteUser.ROLE_RECRUITER)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Record, CreditRecordAdmin)
