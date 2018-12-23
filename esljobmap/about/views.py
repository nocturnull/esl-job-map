# about/views.py

from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms.contact_us import ContactUsForm
from .settings import SITE_CONTACT_EMAIL

from djangomailgun.message.api import MessageApi


class About(TemplateView):
    template_name = 'about/index.html'


class ApplyingForJobs(TemplateView):
    template_name = 'about/applying.html'


class VisaJobType(TemplateView):
    template_name = 'about/visa.html'


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
