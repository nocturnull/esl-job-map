# account/views/recruiter.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages

from ..forms.recruiter import RecruiterCreationForm, RecruiterUpdateForm


class RecruiterSignUp(CreateView):
    form_class = RecruiterCreationForm
    template_name = 'registration/signup/recruiter.html'

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'recruiter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('account_profile')


class EditRecruiterProfile(LoginRequiredMixin, TemplateView):
    template_name = 'account/edit_profile_form.html'
    success_url = reverse_lazy('recruiter_profile_edit')

    def get(self, request, **kwargs):
        user_form = RecruiterUpdateForm(instance=request.user)

        return render(
            request,
            self.template_name,
            {
                'user_form': user_form,
                'notice': 'This information will be used to automatically fill in your job fields'
            }
        )

    def post(self, request, **kwargs):
        user_form = RecruiterUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'Changes saved!')
            return redirect(self.success_url)
        else:
            return render(
                request,
                self.template_name,
                {'forms': [user_form]}
            )
