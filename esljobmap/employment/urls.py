# employment/urls.py

from django.urls import path

from .views.job_seeking import ListFullTimeJobs, ListPartTimeJobs, ApplyToJobPost, ListApplications
from .views.recruitment import CreateJobPost, ListJobPost, ListJobApplicants, EditJobPost, TakeDownJobPost

urlpatterns = [
    # Common urls
    path('full-time-jobs', ListFullTimeJobs.as_view(), name='employment_full_time_jobs'),
    path('part-time-jobs', ListPartTimeJobs.as_view(), name='employment_part_time_jobs'),
    # Recruiter only pages
    path('recruiter/job/post', CreateJobPost.as_view(), name='employment_create_job'),
    path('recruiter/job/my-posts', ListJobPost.as_view(), name='employment_my_job_posts'),
    path('recruiter/job/applicants/<int:pk>', ListJobApplicants.as_view(), name='employment_job_applicants'),
    path('recruiter/job/edit/<int:pk>', EditJobPost.as_view(), name='employment_edit_job_post'),
    path('recruiter/job/take_down/<int:pk>', TakeDownJobPost.as_view(), name='employment_takedown_job_post'),
    # Teacher only pages
    path('teacher/apply/<int:job_post_id>', ApplyToJobPost.as_view(), name='employment_apply_to_job'),
    path('teacher/applications', ListApplications.as_view(), name='employment_applications')
]
