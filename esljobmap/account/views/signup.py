# account/views/signup.py

from django.views.generic import CreateView

from ..forms.user import SiteUserCreationForm


class SignUp(CreateView):
    form_class = SiteUserCreationForm
    template_name = 'registration/signup/index.html'
