# employment/urls.py

from django.urls import path

from .views.recruitment import CreateJobPost, ListJobPost, EditJobPost, TakeDownJobPost

urlpatterns = [
    path('job/create', CreateJobPost.as_view(), name='employment_create_job'),
    path('job/my_posts', ListJobPost.as_view(), name='employment_my_job_posts'),
    path('job/edit/<int:pk>', EditJobPost.as_view(), name='employment_edit_job_post'),
    path('job/take_down/<int:pk>', TakeDownJobPost.as_view(), name='employment_takedown_job_post')
]
