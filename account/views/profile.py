# account/views/profile.py

from django.views.generic import DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from ..models import SiteUser


class ResolveProfile(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_recruiter:
            return reverse_lazy('recruiter_profile_edit')
        return reverse_lazy('applicant_profile_edit')


class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = SiteUser
    success_url = reverse_lazy('home')
    template_name = 'account/profile_confirm_delete.html'

    def get_object(self, queryset=None):
        return self.request.user
