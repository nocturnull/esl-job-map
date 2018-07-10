# employment/urls.py

from django.urls import path

from .views.recruitment import JobPostCreate

urlpatterns = [
    path('job/create', JobPostCreate.as_view(), name='employment_job_create')
]
