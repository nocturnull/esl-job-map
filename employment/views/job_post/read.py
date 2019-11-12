# employment/views/recruiter/job_read.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.shortcuts import render

from employment.mixins.recruiter import IsJobPosterMixin
from employment.models import JobPost, JobApplication
from employment.decorators import recruiter_required


@method_decorator(recruiter_required, name='dispatch')
class ListJobPost(LoginRequiredMixin, ListView):
    """
    View for recruiters to view all their active job posts.
    """
    model = JobPost
    template_name = 'job_post/read/list.html'

    def get_queryset(self):
        return self.request.user.job_posts.all()

    def get(self, request, *args, **kwargs):
        jobs = sorted(self.get_queryset(), key=lambda j: j.reference_date, reverse=True)
        return render(request, self.template_name, {'object_list': jobs})


@method_decorator(recruiter_required, name='dispatch')
class ListJobApplicants(LoginRequiredMixin, IsJobPosterMixin, DetailView):
    """
    View for recruiters to view applicants for their own job posts.
    """
    model = JobPost
    template_name = 'job_post/read/applicants.html'


@method_decorator(recruiter_required, name='dispatch')
class ViewJobPostApplication(LoginRequiredMixin, DetailView):
    model = JobApplication
    template_name = 'job_post/read/view_application.html'
