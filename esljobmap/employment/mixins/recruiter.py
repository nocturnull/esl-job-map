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


class JobPostWriteMixin:
    """Mixin for creating a job post."""

    def create_response(self, request, form, is_full_time):
        """
        Generate a post create response.

        :param request:
        :param form:
        :param is_full_time:
        :return:
        """
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
                    RecordOriginator.create_or_update_post_record(user, is_full_time=arrayed_job.is_full_time)

                return redirect(self.success_url)
            else:
                context['additional_error'] = 'Error: Insufficient job credits'
        return render(request, self.template_name, context=context)

    def repost_response(self, request, form, instance):
        """
        Generate a job repost response.

        :param request:
        :param form:
        :param instance:
        :return:
        """
        user = request.user
        user_regulator = UserTransformer(user)
        context = {'form': form, 'job_post': instance}

        if form.is_valid():
            if user_regulator.can_afford_post():
                arrayed_job = ArrayedJobPost(instance)
                arrayed_job.normalize_location()

                # Relevant job post, credits, and log need to be updated atomically.
                with transaction.atomic():
                    # Save job post.
                    arrayed_job.repost()
                    # Deduct credits from the users account.
                    user_regulator.consume_post_credits()
                    # Track the changes
                    RecordOriginator.create_or_update_post_record(user, is_full_time=arrayed_job.is_full_time)

                return redirect(self.success_url)
            else:
                context['additional_error'] = 'Error: Insufficient job credits'
        return render(request, self.template_name, context=context)
