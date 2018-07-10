# account/views/profile.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from ..models import SiteUser
from ..forms import UserUpdateForm, TeacherUpdateForm


class ViewProfile(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        kwargs['teacher'] = None
        kwargs['edit_url'] = reverse_lazy('recruiter_profile_edit')

        if self.request.user.is_teacher:
            kwargs['teacher'] = self.request.user.teacher
            kwargs['edit_url'] = reverse_lazy('teacher_profile_edit')

        return kwargs


class EditTeacherProfile(LoginRequiredMixin, TemplateView):
    template_name = 'account/edit_profile_form.html'
    success_url = reverse_lazy('account_profile')

    def get(self, request, **kwargs):
        user_form = UserUpdateForm(instance=request.user)
        teacher_form = TeacherUpdateForm(instance=request.user.teacher)

        return render(
            request,
            self.template_name,
            {'forms': [user_form, teacher_form]}
        )

    def post(self, request, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        teacher_form = TeacherUpdateForm(request.POST, instance=request.user.teacher)

        if user_form.is_valid() and teacher_form.is_valid():
            user_form.save()
            teacher_form.save()

            return redirect(self.success_url)
        else:
            return render(
                request,
                self.template_name,
                {'forms': [user_form, teacher_form]}
            )


class EditRecruiterProfile(LoginRequiredMixin, TemplateView):
    template_name = 'account/edit_profile_form.html'
    success_url = reverse_lazy('account_profile')

    def get(self, request, **kwargs):
        user_form = UserUpdateForm(instance=request.user)

        return render(
            request,
            self.template_name,
            {'forms': [user_form]}
        )

    def post(self, request, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

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
