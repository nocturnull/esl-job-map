# employment/urls.py

from django.urls import path

from .views.job_post.update import EditFullTimeJobPost, EditPartTimeJobPost, \
    CloseJobPost, RepostJob
from .views.job_post.create import JobPostIndex, CreateFullTimeJobPost, CreatePartTimeJobPost
from .views.job_post.read import ListJobPost, ListJobApplicants, ViewJobPostApplication
from .views.job_seeking import ApplyToJobPost, RegistrationAfterApplying, ListApplications
from .views.job_metadata import DisinterestedJobPostCreate, DisinterestedJobPostDelete
from .views.map import FullTimeMap, PartTimeMap


urlpatterns = [
    # Common urls
    path('full-time/', FullTimeMap.as_view(), name='employment_full_time_map'),
    path('full-time/<str:city>', FullTimeMap.as_view(), name='employment_full_time_map_city'),
    path('part-time/', PartTimeMap.as_view(), name='employment_part_time_map'),
    path('part-time/<str:city>', PartTimeMap.as_view(), name='employment_part_time_map_city'),
    # Recruiter only pages
    # Create
    path('recruiter/job/post', JobPostIndex.as_view(), name='employment_job_post_index'),
    path('recruiter/job/post/full-time', CreateFullTimeJobPost.as_view(), name='employment_create_full_time_job'),
    path('recruiter/job/post/part-time', CreatePartTimeJobPost.as_view(), name='employment_create_part_time_job'),
    # Read
    path('recruiter/job/my-jobs', ListJobPost.as_view(), name='employment_my_job_posts'),
    path('recruiter/job/applicants/<int:pk>', ListJobApplicants.as_view(), name='employment_job_applicants'),
    path('recruiter/job/application/<int:pk>', ViewJobPostApplication.as_view(), name='employment_view_application'),
    # Update
    path('recruiter/job/edit/full-time/<int:pk>', EditFullTimeJobPost.as_view(), name='employment_edit_full_time_job_post'),
    path('recruiter/job/edit/part-time/<int:pk>', EditPartTimeJobPost.as_view(), name='employment_edit_part_time_job_post'),
    path('recruiter/job/close/<int:pk>', CloseJobPost.as_view(), name='employment_close_job_post'),
    path('recruiter/job/repost/<int:pk>', RepostJob.as_view(), name='employment_repost_job_post'),
    # Teacher only pages
    path('teacher/apply/<int:job_post_id>', ApplyToJobPost.as_view(), name='employment_apply_to_job'),
    path('teacher/applications', ListApplications.as_view(), name='employment_applications'),
    path('teacher/job/not-interested/<int:pk>', DisinterestedJobPostCreate.as_view(), name='employment_track_job_disinterest'),
    path('teacher/job/interested/<int:pk>', DisinterestedJobPostDelete.as_view(), name='employment_remove_job_disinterest'),
    path('teacher/applied/register', RegistrationAfterApplying.as_view(), name='employment_applied_register')
]
