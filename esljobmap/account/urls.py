# account/urls.py

from django.urls import path
from .views.signup import SignUp, TeacherSignUp, RecruiterSignUp
from .views.profile import ViewProfile, EditProfile

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup/teacher', TeacherSignUp.as_view(), name='teacher_signup'),
    path('signup/recruiter', RecruiterSignUp.as_view(), name='recruiter_signup'),
    path('profile', ViewProfile.as_view(), name='account_profile'),
    path('profile/edit', EditProfile.as_view(success_url='/account/profile'), name='account_profile_edit')
]
