# about/urls.py

from django.urls import path

from .views import About, ApplyingForJobs, VisaJobType, ContactUs, ThankYou

urlpatterns = [
    path('', About.as_view(), name='about'),
    path('applying-for-jobs', ApplyingForJobs.as_view(), name='about_applying'),
    path('visa-and-job-type', VisaJobType.as_view(), name='about_visa'),
    path('contact-us', ContactUs.as_view(), name='about_contact_us'),
    path('thank-you', ThankYou.as_view(), name='about_thank_you')
]
