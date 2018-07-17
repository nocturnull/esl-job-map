# employment/urls.py

from django.urls import path

from .views.recruitment import JobPostCreate, JobPostList, EditJobPost

urlpatterns = [
    path('job/create', JobPostCreate.as_view(), name='employment_job_create'),
    path('job/my_posts', JobPostList.as_view(), name='employment_my_job_posts'),
    path('job/edit/<int:pk>', EditJobPost.as_view(), name='employment_edit_job_post')
]
