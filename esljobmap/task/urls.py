# task/urls.py

from django.urls import path

from .views.job_post import DispatchExpiryNotifications
from .views.account import UpdateNames
from .views.token import GenerateToken


urlpatterns = [
    path('auth/grant', GenerateToken.as_view(), name='task_auth_grant'),
    path('job-post/notify-expired', DispatchExpiryNotifications.as_view(), name='task_job_expired_notice'),
    path('account/update-names', UpdateNames.as_view(), name='task_account_names')
]
