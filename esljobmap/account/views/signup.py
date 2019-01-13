# account/views/signup.py

from django.views.generic import CreateView

from ..forms.user import SiteUserCreationForm


class SignUp(CreateView):
    form_class = SiteUserCreationForm
    template_name = 'registration/signup/index.html'
    extra_context = {
        'mtitle': 'ESLJobMap.com - Registration Page',
        'mdescription': 'Register as a teacher to automatically fill in and track your applications, '
                        'or register as a recruiter to post jobs on our site.'
    }
