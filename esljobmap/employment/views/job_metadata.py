# employment/views/job_metadata.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import HttpResponse

from ..models import JobPost, DisinterestedJobPost


class DisinterestedJobPostCreate(LoginRequiredMixin, View):
    """Create a record for a job post disinterest"""
    def get(self, request, pk):
        job_post = JobPost.objects.get(pk=pk)
        user = request.user
        DisinterestedJobPost.objects.create(site_user=user, job_post=job_post)
        return HttpResponse(job_post.build_html_content(user, request))


class DisinterestedJobPostDelete(LoginRequiredMixin, View):
    """Delete a record for a job post disinterest"""
    def get(self, request, pk):
        job_post = JobPost.objects.get(pk=pk)
        user = request.user
        DisinterestedJobPost.objects.filter(site_user=user, job_post=job_post).delete()
        return HttpResponse(job_post.build_html_content(user, request))
