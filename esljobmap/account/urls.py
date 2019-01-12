# account/urls.py

from django.urls import path
from .views.login import SiteUserLogin
from .views.signup import SignUp, ApplicantSignUp, RecruiterSignUp
from .views.profile import ResolveProfile, EditTeacherProfile, EditRecruiterProfile, DeleteProfile

urlpatterns = [
    path('login/', SiteUserLogin.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup/applicant', ApplicantSignUp.as_view(), name='applicant_signup'),
    path('signup/recruiter', RecruiterSignUp.as_view(), name='recruiter_signup'),
    path('profile', ResolveProfile.as_view(), name='account_profile'),
    path('profile/applicant', EditTeacherProfile.as_view(), name='applicant_profile_edit'),
    path('profile/recruiter', EditRecruiterProfile.as_view(), name='recruiter_profile_edit'),
    path('profile/delete', DeleteProfile.as_view(), name='account_profile_delete')
]
