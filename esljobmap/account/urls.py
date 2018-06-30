# account/urls.py

from django.urls import path
from .views.signup import SignUp, TeacherSignUp, RecruiterSignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup/teacher', TeacherSignUp.as_view(), name='teacher_signup'),
    path('signup/recruiter', RecruiterSignUp.as_view(), name='recruiter_signup'),
]
