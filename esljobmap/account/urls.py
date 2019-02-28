# account/urls.py

from django.views.generic import RedirectView
from django.urls import path, reverse_lazy

from .views.recruiter import RecruiterSignUp, EditRecruiterProfile, OptOutExpiredPostNotifications
from .views.applicant import ApplicantSignUp, EditApplicantProfile
from .views.profile import ResolveProfile, DeleteProfile
from .views.login import SiteUserLogin
from .views.signup import SignUp

urlpatterns = [
    path('login/', SiteUserLogin.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup/applicant', ApplicantSignUp.as_view(), name='applicant_signup'),
    path('signup/job-poster', RecruiterSignUp.as_view(), name='recruiter_signup'),
    path('signup/recruiter', RedirectView.as_view(url=reverse_lazy('recruiter_signup'), permanent=False), name='recruiter_former_signup'),
    path('profile', ResolveProfile.as_view(), name='account_profile'),
    path('profile/applicant', EditApplicantProfile.as_view(), name='applicant_profile_edit'),
    path('profile/recruiter', EditRecruiterProfile.as_view(), name='recruiter_profile_edit'),
    path('profile/recruiter/opt-out-expired-notification', OptOutExpiredPostNotifications.as_view(), name='recruiter_opt_out_expired_notif'),
    path('profile/delete', DeleteProfile.as_view(), name='account_profile_delete')
]
