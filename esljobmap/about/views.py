# about/views.py

from django.views.generic import TemplateView


class About(TemplateView):
    template_name = 'about/index.html'


class ApplyingForJobs(TemplateView):
    template_name = 'about/applying.html'


class VisaJobType(TemplateView):
    template_name = 'about/visa.html'
