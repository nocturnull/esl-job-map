# employment/views/recruiter/job_create.py

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.urls import reverse_lazy

from employment.forms.job_post.create import CreateFullTimeJobForm, CreatePartTimeJobForm
from employment.mixins.recruiter import JobPostWriteMixin
from employment.decorators import recruiter_required


@method_decorator(recruiter_required, name='dispatch')
class JobPostIndex(LoginRequiredMixin, TemplateView):
    """
    View that shows options between full time and part time maps.
    """
    template_name = 'job_post/create/index.html'


@method_decorator(recruiter_required, name='dispatch')
class CreateFullTimeJobPost(LoginRequiredMixin, JobPostWriteMixin, TemplateView):
    """
    Job Post creation view.
    """
    template_name = 'map/index.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def get(self, request, *args, **kwargs):
        """
        HTTP GET method simply redirects.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return redirect(reverse_lazy('employment_full_time_map') + "#postAnchor")

    def post(self, request, *args, **kwargs):
        """
        Attempt to create a new full time job post.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.create_response(request, CreateFullTimeJobForm(request.POST), is_full_time=True)


@method_decorator(recruiter_required, name='dispatch')
class CreatePartTimeJobPost(LoginRequiredMixin, JobPostWriteMixin, TemplateView):
    """
    Job Post creation view.
    """
    template_name = 'map/index.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def get(self, request, *args, **kwargs):
        """
        HTTP GET method simply redirects.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return redirect(reverse_lazy('employment_part_time_map') + "#postAnchor")

    def post(self, request, *args, **kwargs):
        """
        Attempt to create a new part time job post.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.create_response(request, CreatePartTimeJobForm(request.POST), is_full_time=False)
