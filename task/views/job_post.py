# task/views/job_post.py

from django.http.response import HttpResponse

from ..resources.job_post.manager import JobPostManager
from .generic import ApiView


class DispatchExpiryNotifications(ApiView):
    """View for sending job post expiry notifications."""

    def get(self, request, *args, **kwargs):
        """
        curl -i -H 'Authorization: {username} {token}' http://{path}/task/job-post/notify-expired

        :return:
        """
        emails_sent = JobPostManager.send_expiry_emails(request)
        return HttpResponse('{}\n'.format(emails_sent))


class UpdatePostedAt(ApiView):
    """View for updating posted at dates."""

    def get(self, request, *args, **kwargs):
        """
        curl -i -H 'Authorization: {username} {token}' http://{path}/task/job-post/update-posted-at

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        updated_jobs = JobPostManager.update_posted_dates()
        return HttpResponse('{}\n'.format(updated_jobs))
