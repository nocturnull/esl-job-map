# employment/views/recruiter/job_create.py

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse_lazy

from employment.forms.job_post.create import CreateFullTimeJobForm, CreatePartTimeJobForm
from employment.managers.post_manager import PostManager
from employment.decorators import recruiter_required
from employment.models import JobPost

from datetime import datetime


@method_decorator(recruiter_required, name='dispatch')
class JobPostIndex(LoginRequiredMixin, TemplateView):
    """
    View that shows options between full time and part time maps.
    """
    template_name = 'job_post/create/index.html'


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
        new_job_post.posted_at = datetime.now()
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
        new_job_post.posted_at = datetime.now()
        new_job_post.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('employment_part_time_map') + "#postAnchor")
