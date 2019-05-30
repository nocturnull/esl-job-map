# account/views/login.py

from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth import login

from ..mixins.is_admin import IsAdminMixin
from ..forms.user import AdminLoginForm
from ..models.user import SiteUser


class SiteUserLogin(LoginView):
    """SiteUser Login View"""
    extra_context = {
        'mtitle': 'Login to ESL Job Map',
        'mdescription': 'Login to your ESL Job Map account.'
    }

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')

        return super(SiteUserLogin, self).get(request, *args, **kwargs)


class AdminUserLogin(IsAdminMixin, TemplateView):
    template_name = 'soomda/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': AdminLoginForm()
        })

    def post(self, request, *args, **kwargs):
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = SiteUser.objects.get(email=email)
                login(self.request, user)
                return redirect('account_profile')
            except SiteUser.DoesNotExist:
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})
