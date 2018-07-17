# employment/urls.py

from django.urls import path

from .views.recruitment import JobPostCreate, JobPostList

urlpatterns = [
    path('job/create', JobPostCreate.as_view(), name='employment_job_create'),
    path('job/my_posts', JobPostList.as_view(), name='employment_my_job_posts')
]
