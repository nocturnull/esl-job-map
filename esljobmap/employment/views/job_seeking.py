# employment/views/job_seeking.py
from django.views.generic import ListView
from ..models import JobPost


class ListFullTimeJobs(ListView):
    model = JobPost
    template_name = 'employment/job_list.html'
    queryset = JobPost.objects.filter(is_full_time=True, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Full Time Jobs'
        return context


class ListPartTimeJobs(ListView):
    model = JobPost
    template_name = 'employment/job_list.html'
    queryset = JobPost.objects.filter(is_full_time=False, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Part Time Jobs'
        return context
