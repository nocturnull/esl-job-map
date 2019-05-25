# employment/views/job_post/delete.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.db import transaction

from employment.mixins.recruiter import IsJobPosterMixin
from employment.decorators import recruiter_required
from employment.models import JobPost

from job_credit.model_generators.history import RecordGenerator


@method_decorator(recruiter_required, name='dispatch')
class DeleteJobPost(LoginRequiredMixin, IsJobPosterMixin, DeleteView):
    model = JobPost
    template_name = 'job_post/delete/index.html'
    success_url = reverse_lazy('employment_my_job_posts')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        with transaction.atomic():
            job_post = self.get_object()
            refund_credits = job_post.calculate_refund()
            request.user.credit_bank.balance += refund_credits
            request.user.credit_bank.save()
            RecordGenerator.track_refund_record(request.user, job_credits=refund_credits)

        return super(DeleteJobPost, self).delete(request, *args, **kwargs)