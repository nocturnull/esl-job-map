# employment/views/recruitment.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from ..models import JobPost
from ..forms.recruitment import JobCreationForm


class JobPostCreate(LoginRequiredMixin, CreateView):
    model = JobPost
    form_class = JobCreationForm
    template_name = 'employment/job_post_form.html'
    success_url = reverse_lazy('account_profile')
