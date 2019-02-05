# employment/views/recruitment.py

from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import F

from ..mixins.recruiter import IsJobPosterMixin
from ..managers.post_manager import PostManager
from ..models import JobPost, JobApplication
from ..decorators import recruiter_required
from ..forms.recruiter import CreateFullTimeJobForm, CreatePartTimeJobForm,\
    EditFullTimeJobForm, EditPartTimeJobForm, TakeDownJobForm, RepostJobForm


@method_decorator(recruiter_required, name='dispatch')
class JobPostIndex(LoginRequiredMixin, TemplateView):
    """
    View that shows options between full time and part time maps.
    """
    template_name = 'recruiter/job_post_index.html'


@method_decorator(recruiter_required, name='dispatch')
class CreateFullTimeJobPost(LoginRequiredMixin, CreateView):
    """
    Job Post creation view.
    """
    model = JobPost
    form_class = CreateFullTimeJobForm
    template_name = 'map/index.html'
    success_url = reverse_lazy('employment_my_job_posts')
    extra_context = {'is_full_time': True}

    def form_valid(self, form):
        new_job_post = form.save(commit=False)
        new_job_post.is_full_time = True

        # Fix location if needed.
        if PostManager.has_existing_location(new_job_post):
            PostManager.offset_location(new_job_post)

        new_job_post.site_user = self.request.user
        new_job_post.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('employment_full_time_map') + "#postAnchor")


@method_decorator(recruiter_required, name='dispatch')
class CreatePartTimeJobPost(LoginRequiredMixin, CreateView):
    """
    Job Post creation view.
    """
    model = JobPost
    form_class = CreatePartTimeJobForm
    template_name = 'map/index.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def form_valid(self, form):
        new_job_post = form.save(commit=False)

        # Fix location if needed.
        if PostManager.has_existing_location(new_job_post):
            PostManager.offset_location(new_job_post)

        new_job_post.site_user = self.request.user
        new_job_post.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('employment_part_time_map') + "#postAnchor")


@method_decorator(recruiter_required, name='dispatch')
class ListJobPost(LoginRequiredMixin, ListView):
    """
    View for recruiters to view all their active job posts.
    """
    model = JobPost
    template_name = 'recruiter/job_post_list.html'

    def get_queryset(self):
        return self.request.user.job_posts.all().order_by(F('created_at').desc(nulls_last=True))


@method_decorator(recruiter_required, name='dispatch')
class ListJobApplicants(LoginRequiredMixin, IsJobPosterMixin, DetailView):
    """
    View for recruiters to view applicants for their own job posts.
    """
    model = JobPost
    template_name = 'recruiter/job_post_applicants.html'


@method_decorator(recruiter_required, name='dispatch')
class EditFullTimeJobPost(LoginRequiredMixin, IsJobPosterMixin, UpdateView):
    """
    View for editing existing full time job posts.

    https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/#performing-extra-work
    """
    model = JobPost
    form_class = EditFullTimeJobForm
    template_name = 'recruiter/job_post_edit.html'
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
    template_name = 'recruiter/job_post_edit.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_url'] = self.request.path
        return context


@method_decorator(recruiter_required, name='dispatch')
class TakeDownJobPost(LoginRequiredMixin, IsJobPosterMixin, UpdateView):
    """
    View for taking down a job post.
    """
    model = JobPost
    form_class = TakeDownJobForm
    template_name = 'recruiter/job_post_confirm_takedown.html'
    success_url = reverse_lazy('employment_my_job_posts')


@method_decorator(recruiter_required, name='dispatch')
class RepostJob(LoginRequiredMixin, IsJobPosterMixin, UpdateView):
    """
    View for reposting a job after taking it down.
    """
    model = JobPost
    form_class = RepostJobForm
    template_name = 'recruiter/job_post_repost_form.html'
    success_url = reverse_lazy('employment_my_job_posts')


@method_decorator(recruiter_required, name='dispatch')
class ViewJobPostApplication(LoginRequiredMixin, DetailView):
    model = JobApplication
    template_name = 'recruiter/job_post_view_application.html'
