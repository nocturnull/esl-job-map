# employment/views/map.py

from django.views.generic import ListView
from django.shortcuts import reverse

from ..forms.recruitment import CreateFullTimeJobForm, CreatePartTimeJobForm
from ..models import JobPost

from cloud.templatetags.remote import cdn_image
from account.templatetags.profile import is_recruiter


class FullTimeMap(ListView):
    model = JobPost
    template_name = 'map/index.html'
    queryset = JobPost.objects.filter(is_full_time=True, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['icon_image'] = cdn_image('koco-man/koco-blue-40x40.png')
        context['disabled_icon_image'] = cdn_image('koco-man/koco-grey-40x40.png')
        context['map_class'] = 'recruiter' if is_recruiter(self.request) else ''
        context['is_full_time'] = True
        context['form'] = CreateFullTimeJobForm()
        context['post_url'] = reverse('employment_create_full_time_job')
        return context


class PartTimeMap(ListView):
    model = JobPost
    template_name = 'map/index.html'
    queryset = JobPost.objects.filter(is_full_time=False, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['icon_image'] = cdn_image('koco-man/koco-orange-40x40.png')
        context['disabled_icon_image'] = cdn_image('koco-man/koco-grey-40x40.png')
        context['map_class'] = 'recruiter' if is_recruiter(self.request) else ''
        context['is_full_time'] = False
        context['post_url'] = reverse('employment_create_part_time_job')
        context['form'] = CreatePartTimeJobForm()
        return context
