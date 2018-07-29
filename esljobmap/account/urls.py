# account/urls.py

from django.urls import path
from .views.login import SiteUserLogin
from .views.signup import SignUp, TeacherSignUp, RecruiterSignUp
from .views.profile import ViewProfile, EditTeacherProfile, EditRecruiterProfile, DeleteProfile

urlpatterns = [
    path('login/', SiteUserLogin.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup/teacher', TeacherSignUp.as_view(), name='teacher_signup'),
    path('signup/recruiter', RecruiterSignUp.as_view(), name='recruiter_signup'),
    path('profile', ViewProfile.as_view(), name='account_profile'),
    path('profile/edit/teacher', EditTeacherProfile.as_view(), name='teacher_profile_edit'),
    path('profile/edit/recruiter', EditRecruiterProfile.as_view(), name='recruiter_profile_edit'),
    path('profile/delete', DeleteProfile.as_view(), name='account_profile_delete')
]
