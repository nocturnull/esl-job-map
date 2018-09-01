# employment/views/job_seeking.py
from django.views.generic import ListView, TemplateView
from django.shortcuts import render

from ..models import JobPost, JobApplication
from ..forms.recruitment import ApplyToJobForm
from ..email.template_manager import TemplateManager as EmailTemplateManager


class ListFullTimeJobs(ListView):
    model = JobPost
    template_name = 'employment/job_list.html'
    queryset = JobPost.objects.filter(is_full_time=True, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['title'] = 'Full-Time Map'
        return context


class ListPartTimeJobs(ListView):
    model = JobPost
    template_name = 'employment/job_list.html'
    queryset = JobPost.objects.filter(is_full_time=False, is_visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We don't want to show jobs that have expired.
        context['object_list'] = [o for o in self.object_list if not o.is_expired]
        context['title'] = 'Part-Time Map'
        return context


class ApplyToJobPost(TemplateView):
    template_name = 'teacher/application_form.html'

    def get(self, request, job_post_id):
        job_post = JobPost.objects.get(pk=job_post_id)
        contact_email = request.user.email if request.user.is_authenticated else ''

        job_form = ApplyToJobForm(initial={
            'title': job_post.title,
            'email_body': EmailTemplateManager.generate_email_body(request.user, job_post),
            'contact_email': contact_email
        })

        return render(request,
                      self.template_name,
                      {
                          'job_post': job_post,
                          'job_form': job_form
                      })

    def post(self, request, job_post_id):
        job_post = JobPost.objects.get(pk=job_post_id)
        job_form = ApplyToJobForm(request.POST, request.FILES)

        if job_form.is_valid():
            kwargs = {
                'job_post': job_post,
                'contact_email': job_form.cleaned_data['contact_email']
            }
            if request.user.is_authenticated:
                kwargs['site_user'] = request.user

            JobApplication.objects.create(**kwargs)

            return render(request,
                          'teacher/application_success.html',
                          {
                              'job_post': job_post
                          })
        else:
            return render(request,
                          self.template_name,
                          {
                              'job_post': job_post,
                              'job_form': job_form
                          })


class ListApplications(ListView):
    model = JobApplication
    template_name = 'teacher/application_list.html'
