# job_credit/admin.py

from django.contrib import admin

from .forms.update import CreditRecordCreationForm
from .models.history import Record


class CreditRecordAdmin(admin.ModelAdmin):
    list_display = ['site_user', 'created_at', 'action', 'amount', 'description']
    form = CreditRecordCreationForm


admin.site.register(Record, CreditRecordAdmin)
