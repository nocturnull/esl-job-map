# employment/views/map.py

from django.views.generic import ListView

from ..forms.recruitment import CreateJobForm
from ..models import JobPost


class FullTimeMap(ListView):
    model = JobPost
    template_name = 'map/index.html'
    queryset = JobPost.objects.filter(is_full_time=True, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['title'] = 'Full-Time Map'
        context['form'] = CreateJobForm()
        return context


class PartTimeMap(ListView):
    model = JobPost
    template_name = 'map/index.html'
    queryset = JobPost.objects.filter(is_full_time=False, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['title'] = 'Part-Time Map'
        context['form'] = CreateJobForm()
        return context
