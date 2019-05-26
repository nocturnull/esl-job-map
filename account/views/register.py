# account/views/register.py

from django.views.generic import CreateView

from ..forms.user import SiteUserCreationForm


class Register(CreateView):
    form_class = SiteUserCreationForm
    template_name = 'registration/register/index.html'
    extra_context = {
        'mtitle': 'Register as a Teacher or Recruiter on ESL Job Map',
        'mdescription': 'Register as a teacher to automatically fill in and track your applications, '
                        'or register as a recruiter to post jobs on our site.'
    }
