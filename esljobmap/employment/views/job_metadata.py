# employment/views/job_metadata.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponseRedirect

from ..models import JobPost, DisinterestedJobPost


class DisinterestedJobPostCreate(LoginRequiredMixin, View):
    """Create a record for a job post disinterest"""
    def get(self, request, pk):
        job_post = JobPost.objects.get(pk=pk)
        DisinterestedJobPost.objects.create(site_user=request.user, job_post=job_post)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class DisinterestedJobPostDelete(LoginRequiredMixin, View):
    """Delete a record for a job post disinterest"""
    def get(self, request, pk):
        job_post = JobPost.objects.get(pk=pk)
        DisinterestedJobPost.objects.filter(site_user=request.user, job_post=job_post).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
