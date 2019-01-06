# employment/views/map.py

from django.views.generic import ListView
from django.shortcuts import reverse

from ..forms.recruitment import CreateFullTimeJobForm, CreatePartTimeJobForm
from ..models import JobPost
from ..managers.map_manager import MapManager

from account.templatetags.profile import is_recruiter
from blanket.session_manager import SessionManager
from cloud.templatetags.remote import cdn_image


class FullTimeMap(ListView):
    model = JobPost
    template_name = 'map/index.html'
    queryset = JobPost.objects.filter(is_full_time=True, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            city = self.kwargs['city']
        except KeyError:
            city = ''

        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['icon_image'] = cdn_image('koco-man/blue-60x60.png')
        context['marker_image'] = cdn_image('marker/blue.png')
        context['map_class'] = 'recruiter' if is_recruiter(self.request) else ''
        context['is_full_time'] = True
        context['form'] = CreateFullTimeJobForm(self.request)
        context['post_url'] = reverse('employment_create_full_time_job')
        context['location'] = MapManager.resolve_location_data(self.request, city)
        context['show_warning'] = SessionManager.needs_full_time_warning(self.request)

        return context


class PartTimeMap(ListView):
    model = JobPost
    template_name = 'map/index.html'
    queryset = JobPost.objects.filter(is_full_time=False, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            city = self.kwargs['city']
        except KeyError:
            city = ''

        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['icon_image'] = cdn_image('koco-man/orange-30x30.png')
        context['marker_image'] = cdn_image('marker/orange.png')
        context['map_class'] = 'recruiter' if is_recruiter(self.request) else ''
        context['is_full_time'] = False
        context['form'] = CreatePartTimeJobForm(self.request)
        context['post_url'] = reverse('employment_create_part_time_job')
        context['location'] = MapManager.resolve_location_data(self.request, city)
        context['show_warning'] = SessionManager.needs_part_time_warning(   self.request)

        return context
