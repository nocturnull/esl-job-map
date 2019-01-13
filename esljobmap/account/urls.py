# account/urls.py

from django.urls import path
from .views.signup import SignUp
from .views.login import SiteUserLogin
from .views.applicant import ApplicantSignUp
from .views.recruiter import RecruiterSignUp
from .views.profile import ResolveProfile, DeleteProfile
from .views.applicant import EditApplicantProfile
from .views.recruiter import EditRecruiterProfile

urlpatterns = [
    path('login/', SiteUserLogin.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup/applicant', ApplicantSignUp.as_view(), name='applicant_signup'),
    path('signup/recruiter', RecruiterSignUp.as_view(), name='recruiter_signup'),
    path('profile', ResolveProfile.as_view(), name='account_profile'),
    path('profile/applicant', EditApplicantProfile.as_view(), name='applicant_profile_edit'),
    path('profile/recruiter', EditRecruiterProfile.as_view(), name='recruiter_profile_edit'),
    path('profile/delete', DeleteProfile.as_view(), name='account_profile_delete')
]
