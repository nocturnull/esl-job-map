# employment/mixins/recruiter.py

from django.http.response import HttpResponseForbidden


class IsJobPosterMixin:

    def dispatch(self, request, *args, **kwargs):
        job_post = self.get_object()
        if job_post.is_job_poster(request.user):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()
