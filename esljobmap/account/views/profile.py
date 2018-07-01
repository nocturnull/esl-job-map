# account/views/profile.py

from django.views.generic import TemplateView, UpdateView

from ..models import SiteUser


class ViewProfile(TemplateView):
    template_name = 'account/profile.html'


class EditProfile(UpdateView):
    template_name = 'account/edit_profile_form.html'
    model = SiteUser
    fields = ['first_name', 'last_name', 'email', 'phone_number']

    def get_object(self, queryset=None):
        return self.request.user
