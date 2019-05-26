# account/views/password.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages


class ChangePassword(LoginRequiredMixin, TemplateView):
    template_name = 'registration/password_change_form.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully!')
            if self.request.user.is_recruiter:
                return redirect(reverse_lazy('recruiter_profile_edit'))
            return redirect(reverse_lazy('applicant_profile_edit'))
        return render(request, self.template_name, {'form': form})
