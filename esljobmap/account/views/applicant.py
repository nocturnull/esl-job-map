# account/views/applicant.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages

from ..forms.applicant import ApplicantCreationForm
from ..forms.applicant import ApplicantUpdateForm
from ..helpers.applicant import ProfileHelper
from ..forms.user import UserUpdateForm


class ApplicantSignUp(CreateView):
    form_class = ApplicantCreationForm
    template_name = 'registration/signup/applicant.html'
    extra_context = {
        'mtitle': 'Register as a Teacher on ESL Job Map',
        'mdescription': 'Creating an account will allow you to automatically attach your resume, '
                        'fill in information on your cover letter and track jobs you have applied to.'
    }

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('account_profile')


class EditApplicantProfile(LoginRequiredMixin, TemplateView):
    template_name = 'account/edit_profile_form.html'
    success_url = reverse_lazy('applicant_profile_edit')

    def get(self, request, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        applicant_form = ApplicantUpdateForm(instance=request.user.teacher)

        return render(
            request,
            self.template_name,
            {
                'user_form': user_form,
                'applicant_form': applicant_form,
                'notice': 'This information will be used to automatically fill in your cover letters'
            }
        )

    def post(self, request, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        applicant_form = ApplicantUpdateForm(request.POST, request.FILES, instance=request.user.teacher)

        if user_form.is_valid() and applicant_form.is_valid():
            resume = applicant_form.cleaned_data.get('resume_file', None)
            photo = applicant_form.cleaned_data.get('photo_file', None)

            user_form.save()
            applicant = applicant_form.save()

            # Attempt to update resume and profile photo.
            ProfileHelper.save_resume(applicant, resume)
            ProfileHelper.save_photo(applicant, photo)

            messages.success(request, 'Changes saved!')
            return redirect(self.success_url)
        else:
            return render(
                request,
                self.template_name,
                {
                    'user_form': user_form,
                    'applicant_form': applicant_form
                 }
            )
