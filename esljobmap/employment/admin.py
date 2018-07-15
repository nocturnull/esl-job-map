from django.contrib import admin

from .models.recruitment import JobPost


class JobPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'class_type', 'contact_email', 'is_full_time']


admin.site.register(JobPost, JobPostAdmin)
