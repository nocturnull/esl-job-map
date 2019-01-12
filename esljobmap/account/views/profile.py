# account/views/profile.py

from django.views.generic import TemplateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from cloud.file_manager import FileManager
from ..models import SiteUser
from ..models import Resume
from ..forms.user import UserUpdateForm
from ..forms.applicant import ApplicantUpdateForm
from ..forms.recruiter import RecruiterUpdateForm


class ResolveProfile(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_recruiter:
            return reverse_lazy('recruiter_profile_edit')
        return reverse_lazy('applicant_profile_edit')


class EditTeacherProfile(LoginRequiredMixin, TemplateView):
    template_name = 'account/edit_profile_form.html'
    success_url = reverse_lazy('applicant_profile_edit')

    def get(self, request, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        teacher_form = ApplicantUpdateForm(instance=request.user.teacher)

        return render(
            request,
            self.template_name,
            {
                'user_form': user_form,
                'teacher_form': teacher_form,
                'notice': 'This information will be used to automatically fill in your cover letters'
            }
        )

    def post(self, request, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        teacher_form = ApplicantUpdateForm(request.POST, request.FILES, instance=request.user.teacher)
        file_manager = FileManager()

        if user_form.is_valid() and teacher_form.is_valid():
            resume = teacher_form.cleaned_data.get('resume_filename', None)

            user_form.save()
            teacher = teacher_form.save()

            # Attempt to upload new resume if necessary.
            if resume:
                new_resume = Resume.create_resume(filename=resume.name)
                file_manager.upload_file(new_resume.storage_path, resume)
                teacher.resume = new_resume
                teacher.save()

            messages.success(request, 'Changes saved!')
            return redirect(self.success_url)
        else:
            return render(
                request,
                self.template_name,
                {
                    'user_form': user_form,
                    'teacher_form': teacher_form
                 }
            )


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


class DeleteProfile(LoginRequiredMixin, DeleteView):
    model = SiteUser
    success_url = reverse_lazy('home')
    template_name = 'account/profile_confirm_delete.html'

    def get_object(self, queryset=None):
        return self.request.user
