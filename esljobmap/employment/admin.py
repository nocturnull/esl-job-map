# employment/admin.py

from datetime import date

from django.contrib import admin

from .models import JobPost, JobApplication
from .forms.job_post.update import AdminEditJobForm


class CreateDateListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Date Posted'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'created_at'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('prelaunch', 'Pre-launch Posts'),
            ('postlaunch', 'Post-launch Posts'),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'prelaunch':
            return queryset.filter(created_at__lt=date(2019, 1, 19), is_visible=True)
        if self.value() == 'postlaunch':
            return queryset.filter(created_at__gte=date(2019, 1, 19), is_visible=True)


class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'local_created_at', 'site_user_email', 'job_type', 'is_taken_down', 'is_expired',
                    'is_recruiter_banned', 'was_reposted', 'applicant_count']
    list_filter = (CreateDateListFilter, )
    ordering = ['-created_at']
    form = AdminEditJobForm
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        created_override = form.cleaned_data['created_at_override']
        if created_override:
            print(created_override)
            obj.created_at = created_override
        super().save_model(request, obj, form, change)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['contact_email', 'local_created_at', 'job_post']
    fields = ('contact_email', 'cover_letter')
    ordering = ['-created_at']


admin.site.register(JobPost, JobPostAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
