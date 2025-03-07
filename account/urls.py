# account/urls.py

from django.views.generic import RedirectView
from django.urls import path, reverse_lazy

from .views.recruiter import RecruiterRegister, RecruiterProfile, \
    EditRecruiterProfile, OptOutExpiredPostNotifications, EditAutofillOptions
from .views.applicant import ApplicantRegister, EditApplicantProfile
from .views.profile import ResolveProfile, DeleteProfile
from .views.login import SiteUserLogin, AdminUserLogin
from .views.password import ChangePassword
from .views.register import Register

urlpatterns = [
    path('login/', SiteUserLogin.as_view(), name='login'),
    path('soomda/', AdminUserLogin.as_view(), name='soomda'),

    path('register/', Register.as_view(), name='register'),
    # /signup redirect to /register
    path('signup/', RedirectView.as_view(url=reverse_lazy('register'), permanent=False)),

    path('register/applicant', ApplicantRegister.as_view(), name='applicant_register'),
    # /signup/applicant redirect to /register/applicant
    path('signup/applicant', RedirectView.as_view(url=reverse_lazy('applicant_register'), permanent=False)),

    path('register/job-poster', RecruiterRegister.as_view(), name='recruiter_register'),
    # /signup/job-poster redirect to /register/job-poster
    path('signup/job-poster', RedirectView.as_view(url=reverse_lazy('recruiter_register'), permanent=False)),
    # /signup/recruiter redirect to /signup/job-poster
    path('signup/recruiter', RedirectView.as_view(url=reverse_lazy('recruiter_register'), permanent=False)),

    path('profile', ResolveProfile.as_view(), name='account_profile'),
    path('profile/applicant', EditApplicantProfile.as_view(), name='applicant_profile_edit'),
    path('profile/recruiter', RecruiterProfile.as_view(), name='recruiter_profile'),
    path('profile/recruiter/edit', EditRecruiterProfile.as_view(), name='recruiter_profile_edit'),
    path('profile/recruiter/autofill-options', EditAutofillOptions.as_view(), name='recruiter_autofill_options'),
    path('profile/recruiter/opt-out-expired-notification', OptOutExpiredPostNotifications.as_view(), name='recruiter_opt_out_expired_notif'),
    path('profile/delete', DeleteProfile.as_view(), name='account_profile_delete'),
    path('profile/change-password', ChangePassword.as_view(), name='account_change_password')
]
