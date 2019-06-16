# employment/admin.py

from django.db.models import Q
from django.contrib import admin

from .models import JobPost, JobApplication
from .forms.job_post.update import AdminEditJobForm


class ApplicantsFilter(admin.SimpleListFilter):
    title = 'Applicant Status'
    parameter_name = 'site_user'

    def lookups(self, request, model_admin):
        return (
            ('regular', 'Regular Applications'),
            ('filtered', 'Filtered Applications')
        )

    def queryset(self, request, queryset):
        if self.value() == 'regular':
            return queryset.filter(Q(site_user__is_banned=False) | Q(site_user__isnull=True))
        if self.value() == 'filtered':
            return queryset.filter(site_user__is_banned=True)


class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'last_posted_date', 'site_user_email', 'job_type', 'status',
                    'repost_state', 'applicant_count']
    ordering = ['-posted_at']
    form = AdminEditJobForm
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        created_override = form.cleaned_data['created_at_override']
        if created_override:
            obj.created_at = created_override
            obj.created_at_override = None
        super().save_model(request, obj, form, change)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['contact_email', 'local_created_at', 'visa', 'nation', 'job_post']
    list_filter = (ApplicantsFilter, )
    fields = ('contact_email', 'cover_letter')
    ordering = ['-created_at']


admin.site.register(JobPost, JobPostAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
