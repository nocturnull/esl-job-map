# account/views/login.py

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class SiteUserLogin(LoginView):
    """SiteUser Login View"""
    extra_context = {
        'mtitle': 'ESLJobMap.com - Login Page',
        'mdescription': 'Login to your ESL Job Map account.'
    }

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')

        return super(SiteUserLogin, self).get(request, *args, **kwargs)
