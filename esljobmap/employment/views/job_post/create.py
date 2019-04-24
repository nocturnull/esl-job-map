# employment/views/recruiter/job_create.py

from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db import transaction

from employment.forms.job_post.create import CreateFullTimeJobForm, CreatePartTimeJobForm
from employment.model_decorators.job_post import ArrayedJobPost
from employment.decorators import recruiter_required
from employment.models import JobPost

from account.model_regulators.user import UserTransformer

from job_credit.model_generators.history import RecordOriginator

from datetime import datetime


@method_decorator(recruiter_required, name='dispatch')
class JobPostIndex(LoginRequiredMixin, TemplateView):
    """
    View that shows options between full time and part time maps.
    """
    template_name = 'job_post/create/index.html'


@method_decorator(recruiter_required, name='dispatch')
class CreateFullTimeJobPost(LoginRequiredMixin, TemplateView):
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
        Attempt to create a new job post.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        form = CreateFullTimeJobForm(request.POST)
        user = request.user
        user_regulator = UserTransformer(user)
        context = {'form': form, 'is_full_time': True}

        if form.is_valid():
            if user_regulator.can_afford_post():
                arrayed_job = ArrayedJobPost(form.save(commit=False))
                arrayed_job.normalize_location()

                # Relevant job post, credits, and log need to be updated atomically.
                with transaction.atomic():
                    # Save new job post.
                    arrayed_job.create(is_full_time=True, user=request.user)
                    # Deduct credits from the users account.
                    user_regulator.consume_post_credits()
                    # Track the changes
                    RecordOriginator.create_post_record(user, is_consumption=True, is_full_time=True)

                return redirect(self.success_url)
            else:
                context['additional_error'] = 'Error: Insufficient job credits'
        return render(request, self.template_name, context=context)


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

        # # Fix location if needed.
        # if PostManager.has_existing_location(new_job_post):
        #     PostManager.offset_location(new_job_post)

        new_job_post.site_user = self.request.user
        new_job_post.posted_at = datetime.now()
        new_job_post.save()

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect(reverse_lazy('employment_part_time_map') + "#postAnchor")
