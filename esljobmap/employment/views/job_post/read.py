# employment/views/recruiter/job_read.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.db.models import F

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
        return self.request.user.job_posts.all().order_by(F('created_at').desc(nulls_last=True))


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
