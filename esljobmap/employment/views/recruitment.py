# employment/views/recruitment.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from ..models import JobPost
from ..forms.recruitment import JobCreationForm


class JobPostCreate(LoginRequiredMixin, CreateView):
    """
    Job Post creation view.
    """
    model = JobPost
    form_class = JobCreationForm
    template_name = 'employment/job_post_form.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def form_valid(self, form):
        new_job_post = form.save(commit=False)
        new_job_post.site_user = self.request.user
        new_job_post.save()
        return super().form_valid(form)


class JobPostList(LoginRequiredMixin, ListView):
    """
    View for recruiters to view all their job posts.
    """
    model = JobPost
    template_name = 'employment/recruiter_job_list.html'

    def get_queryset(self):
        return self.request.user.job_posts.all()


class EditJobPost(LoginRequiredMixin, UpdateView):
    """
    View for editing existing job posts.

    https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/#performing-extra-work
    """
    model = JobPost
    form_class = JobCreationForm
    template_name = 'employment/job_post_form.html'
    success_url = reverse_lazy('employment_my_job_posts')
