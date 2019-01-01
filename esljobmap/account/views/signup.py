# account/views/signup.py

from django.contrib.auth import login
from django.shortcuts import redirect
from django.views import generic

from ..forms import SiteUserCreationForm, SiteUserTeacherCreationForm, SiteUserRecruiterCreationForm


class SignUp(generic.CreateView):
    form_class = SiteUserCreationForm
    template_name = 'registration/signup/index.html'


class TeacherSignUp(generic.CreateView):
    form_class = SiteUserTeacherCreationForm
    template_name = 'registration/signup/teacher.html'

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('account_profile')


class RecruiterSignUp(generic.CreateView):
    form_class = SiteUserRecruiterCreationForm
    template_name = 'registration/signup/recruiter.html'

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'recruiter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('account_profile')
