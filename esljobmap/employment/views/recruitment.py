# employment/views/recruitment.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from ..models import JobPost


class JobPostCreate(LoginRequiredMixin, CreateView):
    model = JobPost
    template_name = 'employment/job_post_form.html'
    fields = ['title', 'class_type', 'location', 'contact_name', 'contact_email',
              'contact_number', 'schedule', 'other_requirements', 'is_full_time']
    success_url = reverse_lazy('account_profile')
