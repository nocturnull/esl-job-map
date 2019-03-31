# task/urls.py

from django.urls import path

from .views.job_post import DispatchExpiryNotifications, UpdatePostedAt
# from .views.applicant import SendApplicationEmails
# from .views.account import UpdateNames
# from .views.token import GenerateToken


urlpatterns = [
    # path('auth/grant', GenerateToken.as_view(), name='task_auth_grant'),
    path('job-post/notify-expired', DispatchExpiryNotifications.as_view(), name='task_job_expired_notice'),
    path('job-post/update-posted-at', UpdatePostedAt.as_view(), name='task_job_posted_at'),
    # path('account/update-names', UpdateNames.as_view(), name='task_account_names'),
    # path('employment/send-application-emails', SendApplicationEmails.as_view(), name='task_application_emails')
]
