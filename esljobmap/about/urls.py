# about/urls.py

from django.urls import path

from .views import About, ApplyingForJobs, VisaJobType

urlpatterns = [
    path('', About.as_view(), name='about'),
    path('applying-for-jobs', ApplyingForJobs.as_view(), name='about_applying'),
    path('visa-and-job-type', VisaJobType.as_view(), name='about_visa')
]
