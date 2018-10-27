# employment/urls.py

from django.urls import path

from .views.map import FullTimeMap, PartTimeMap
from .views.job_seeking import ApplyToJobPost, ListApplications
from .views.recruitment import CreateFullTimeJobPost, CreatePartTimeJobPost, ListJobPost,\
    EditFullTimeJobPost, EditPartTimeJobPost, ListJobApplicants, TakeDownJobPost

urlpatterns = [
    # Common urls
    path('full-time', FullTimeMap.as_view(), name='employment_full_time_map'),
    path('part-time', PartTimeMap.as_view(), name='employment_part_time_map'),
    # Recruiter only pages
    path('recruiter/job/post/full-time', CreateFullTimeJobPost.as_view(), name='employment_create_full_time_job'),
    path('recruiter/job/post/part-time', CreatePartTimeJobPost.as_view(), name='employment_create_part_time_job'),
    path('recruiter/job/my-jobs', ListJobPost.as_view(), name='employment_my_job_posts'),
    path('recruiter/job/applicants/<int:pk>', ListJobApplicants.as_view(), name='employment_job_applicants'),
    path('recruiter/job/edit/full-time/<int:pk>', EditFullTimeJobPost.as_view(), name='employment_edit_full_time_job_post'),
    path('recruiter/job/edit/part-time/<int:pk>', EditPartTimeJobPost.as_view(), name='employment_edit_part_time_job_post'),
    path('recruiter/job/take_down/<int:pk>', TakeDownJobPost.as_view(), name='employment_takedown_job_post'),
    # Teacher only pages
    path('teacher/apply/<int:job_post_id>', ApplyToJobPost.as_view(), name='employment_apply_to_job'),
    path('teacher/applications', ListApplications.as_view(), name='employment_applications')
]
