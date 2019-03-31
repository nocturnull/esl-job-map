# employment/views/recruiter/job_update.py

from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from employment.forms.job_post.update import EditFullTimeJobForm, EditPartTimeJobForm, \
    CloseJobForm, RestoreJobForm, RepostJobForm
from employment.mixins.recruiter import IsJobPosterMixin
from employment.decorators import recruiter_required
from employment.models import JobPost


@method_decorator(recruiter_required, name='dispatch')
class EditFullTimeJobPost(LoginRequiredMixin, IsJobPosterMixin, UpdateView):
    """
    View for editing existing full time job posts.

    https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/#performing-extra-work
    """
    model = JobPost
    form_class = EditFullTimeJobForm
    template_name = 'job_post/update/edit.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_full_time'] = True
        context['post_url'] = self.request.path
        return context


@method_decorator(recruiter_required, name='dispatch')
class EditPartTimeJobPost(LoginRequiredMixin, IsJobPosterMixin, UpdateView):
    """
    View for editing existing part time job posts.

    https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/#performing-extra-work
    """
    model = JobPost
    form_class = EditPartTimeJobForm
    template_name = 'job_post/update/edit.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_url'] = self.request.path
        return context


@method_decorator(recruiter_required, name='dispatch')
class CloseJobPost(LoginRequiredMixin, IsJobPosterMixin, UpdateView):
    """
    View for closing  a job post.
    """
    model = JobPost
    form_class = CloseJobForm
    template_name = 'job_post/update/close_form.html'
    success_url = reverse_lazy('employment_my_job_posts')


@method_decorator(recruiter_required, name='dispatch')
class RestoreJob(LoginRequiredMixin, IsJobPosterMixin, UpdateView):
    """
    View for reposting a job after taking it down.
    """
    model = JobPost
    form_class = RestoreJobForm
    template_name = 'job_post/update/restore_form.html'
    success_url = reverse_lazy('employment_my_job_posts')


@method_decorator(recruiter_required, name='dispatch')
class RepostJob(LoginRequiredMixin, IsJobPosterMixin, DetailView):
    """
    View for reposting a job after taking it down.
    """
    model = JobPost
    template_name = 'job_post/update/repost_form.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def get(self, request, pk):
        job_post = JobPost.objects.get(id=pk)
        form = RepostJobForm(request.POST)
        return render(request, self.template_name, {'form': form, 'job_post': job_post})

    def post(self, request, pk):
        job_post = JobPost.objects.get(id=pk)
        form = RepostJobForm(request.POST)
        if form.is_valid():
            job_post.reposted_at = datetime.now()
            job_post.posted_at = job_post.reposted_at
            job_post.expiry_notice_sent = False
            job_post.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
