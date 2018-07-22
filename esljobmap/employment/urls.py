# employment/urls.py

from django.urls import path

from .views.job_seeking import ListFullTimeJobs, ListPartTimeJobs
from .views.recruitment import CreateJobPost, ListJobPost, EditJobPost, TakeDownJobPost

urlpatterns = [
    path('full-time-jobs', ListFullTimeJobs.as_view(), name='employment_full_time_jobs'),
    path('part-time-jobs', ListPartTimeJobs.as_view(), name='employment_part_time_jobs'),
    path('job/post', CreateJobPost.as_view(), name='employment_create_job'),
    path('job/my-posts', ListJobPost.as_view(), name='employment_my_job_posts'),
    path('job/edit/<int:pk>', EditJobPost.as_view(), name='employment_edit_job_post'),
    path('job/take_down/<int:pk>', TakeDownJobPost.as_view(), name='employment_takedown_job_post')
]
