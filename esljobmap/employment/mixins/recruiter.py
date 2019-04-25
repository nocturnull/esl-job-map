# employment/mixins/recruiter.py

from job_credit.model_generators.history import RecordOriginator
from employment.model_decorators.job_post import ArrayedJobPost
from account.model_regulators.user import UserTransformer

from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.db import transaction


class IsJobPosterMixin:
    """Mixin to check job poster permissions."""

    def dispatch(self, request, *args, **kwargs):
        job_post = self.get_object()
        if job_post.is_job_poster(request.user):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()


class JobPostCreateMixin:
    """Mixin for creating a job post."""

    def create_response(self, request, form, is_full_time):
        user = request.user
        user_regulator = UserTransformer(user)
        context = {'form': form, 'is_full_time': is_full_time}

        if form.is_valid():
            if user_regulator.can_afford_post():
                arrayed_job = ArrayedJobPost(form.save(commit=False))
                arrayed_job.normalize_location()

                # Relevant job post, credits, and log need to be updated atomically.
                with transaction.atomic():
                    # Save new job post.
                    arrayed_job.create(is_full_time=is_full_time, user=request.user)
                    # Deduct credits from the users account.
                    user_regulator.consume_post_credits()
                    # Track the changes
                    RecordOriginator.create_or_update_post_record(user, is_full_time=is_full_time)

                return redirect(self.success_url)
            else:
                context['additional_error'] = 'Error: Insufficient job credits'
        return render(request, self.template_name, context=context)
