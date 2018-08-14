# employment/views/recruitment.py
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse_lazy

from ..models import JobPost
from ..decorators import recruiter_required
from ..forms.recruitment import CreateJobForm, TakeDownJobForm


@method_decorator(recruiter_required, name='dispatch')
class CreateJobPost(LoginRequiredMixin, CreateView):
    """
    Job Post creation view.
    """
    model = JobPost
    form_class = CreateJobForm
    template_name = 'recruiter/job_post_form.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def form_valid(self, form):
        new_job_post = form.save(commit=False)
        new_job_post.site_user = self.request.user
        new_job_post.save()
        return super().form_valid(form)


@method_decorator(recruiter_required, name='dispatch')
class ListJobPost(LoginRequiredMixin, ListView):
    """
    View for recruiters to view all their job posts.
    """
    model = JobPost
    template_name = 'recruiter/job_post_list.html'

    def get_queryset(self):
        return self.request.user.job_posts.all()


@method_decorator(recruiter_required, name='dispatch')
class ListJobApplicants(LoginRequiredMixin, DetailView):
    """
    View for recruiters to view applicants for their own job posts.
    """
    model = JobPost
    template_name = 'recruiter/job_post_applicants.html'


@method_decorator(recruiter_required, name='dispatch')
class EditJobPost(LoginRequiredMixin, UpdateView):
    """
    View for editing existing job posts.

    https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/#performing-extra-work
    """
    model = JobPost
    form_class = CreateJobForm
    template_name = 'recruiter/job_post_form.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.is_editable:
            return super().get(request, *args, **kwargs)
        return redirect('employment_my_job_posts')


@method_decorator(recruiter_required, name='dispatch')
class TakeDownJobPost(LoginRequiredMixin, UpdateView):
    """
    View for taking down a job post.
    """
    model = JobPost
    form_class = TakeDownJobForm
    template_name = 'recruiter/job_post_confirm_takedown.html'
    success_url = reverse_lazy('employment_my_job_posts')
