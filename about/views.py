# about/views.py

from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms.contact_us import ContactUsForm
from .settings import SITE_CONTACT_EMAIL

from djangomailgun.message.api import MessageApi


class About(TemplateView):
    template_name = 'about/index.html'
    extra_context = {
        'mtitle': 'Learn About ESL Job Map',
        'mdescription': 'ESL Job Map is a map-based English job teaching board for South Korea. '
                        'We have both full and part-time English teaching job maps.'
    }


class ApplyingForJobs(TemplateView):
    template_name = 'about/applying.html'
    extra_context = {
        'mtitle': 'How to Apply for English Teaching Jobs in South Korea',
        'mdescription': 'Documents and qualifications needed for applying to full-time and '
                        'part-time English teaching jobs in South Korea.'
    }


class VisaJobType(TemplateView):
    template_name = 'about/visa.html'
    extra_context = {
        'mtitle': 'South Korea Visa Types for English Teaching and Tutoring',
        'mdescription': 'What you need to be eligible for visa sponsorship to teach English in Korea, '
                        'and what types of English teaching you can do based on your visa type.'
    }


class ContactUs(FormView):
    template_name = 'about/contact_us_form.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('about_thank_you')

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        message_api = MessageApi()
        message_api.send(recipient=SITE_CONTACT_EMAIL,
                         subject=form.cleaned_data['subject'],
                         body=form.cleaned_data['message'],
                         reply_to=form.cleaned_data['email'])

        return HttpResponseRedirect(self.get_success_url())


class ThankYou(TemplateView):
    template_name = 'about/thank_you.html'


class PrivacyPolicy(TemplateView):
    template_name = 'about/privacy_policy.html'


class TermsAndConditions(TemplateView):
    template_name = 'about/terms_and_conditions.html'
