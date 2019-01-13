# employment/views/map.py

from django.views.generic import ListView
from django.urls import reverse_lazy

from ..forms.recruiter import CreateFullTimeJobForm, CreatePartTimeJobForm
from ..models import JobPost
from ..managers.map_manager import MapManager

from account.templatetags.profile import is_recruiter
from blanket.session_manager import SessionManager
from cloud.templatetags.remote import cdn_image


class FullTimeMap(ListView):
    model = JobPost
    template_name = 'map/index.html'
    queryset = JobPost.objects.filter(is_full_time=True, is_visible=True)
    extra_context = {
        'is_full_time': True,
        'mtitle': 'ESLJobMap.com - Full-Time Korea Job Map',
        'mdescription': 'The latest full-time English teaching jobs in Korea, on a map. '
                        'Quickly view work schedule, salary and benefits.',
        'icon_image': cdn_image('koco-man/blue-60x60.png'),
        'marker_image': cdn_image('marker/full-time-60x60.png'),
        'post_url': reverse_lazy('employment_create_full_time_job')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            city = self.kwargs['city']
        except KeyError:
            city = ''

        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['map_class'] = 'recruiter' if is_recruiter(self.request) else ''
        context['form'] = CreateFullTimeJobForm(self.request)
        context['location'] = MapManager.resolve_location_data(self.request, city)
        context['show_warning'] = SessionManager.needs_full_time_warning(self.request)

        return context


class PartTimeMap(ListView):
    model = JobPost
    template_name = 'map/index.html'
    queryset = JobPost.objects.filter(is_full_time=False, is_visible=True)
    extra_context = {
        'is_full_time': False,
        'mtitle': 'ESLJobMap.com - Part-Time Korea Job Map',
        'mdescription': 'The latest part-time English teaching and tutoring jobs in Korea, on a map. '
                        'Quickly view days, hours and pay rate.',
        'icon_image': cdn_image('koco-man/orange-60x60.png'),
        'marker_image': cdn_image('marker/part-time-60x60.png'),
        'post_url': reverse_lazy('employment_create_part_time_job')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            city = self.kwargs['city']
        except KeyError:
            city = ''

        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['map_class'] = 'recruiter' if is_recruiter(self.request) else ''
        context['form'] = CreatePartTimeJobForm(self.request)
        context['location'] = MapManager.resolve_location_data(self.request, city)
        context['show_warning'] = SessionManager.needs_part_time_warning(   self.request)

        return context
