# employment/views/job_seeking.py
from django.views.generic import ListView, TemplateView
from django.shortcuts import render

from djangomailgun.message.api import MessageApi
from cloud.file_manager import FileManager
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
        template = self.template_name
        job_form = ApplyToJobForm(initial={
            'title': job_post.title,
            'email_body': EmailTemplateManager.generate_email_body(request.user, job_post),
            'contact_email': contact_email
        })

        if job_post.has_applicant_applied(request.user):
            template = 'teacher/application_applied.html'

        return render(request,
                      template,
                      {
                          'job_post': job_post,
                          'job_form': job_form
                      })

    def post(self, request, job_post_id):
        job_post = JobPost.objects.get(pk=job_post_id)
        job_form = ApplyToJobForm(request.POST, request.FILES)
        message_api = MessageApi()
        file_manager = FileManager()

        if job_form.is_valid():
            applicant_email = job_form.cleaned_data['contact_email']
            resume = job_form.cleaned_data.get('resume', None)
            kwargs = {
                'job_post': job_post,
                'contact_email': applicant_email,
                'resume_filename': resume.name
            }
            if request.user.is_authenticated:
                kwargs['site_user'] = request.user

            application = JobApplication.objects.create(**kwargs)
            file_manager.upload_file(application.storage_path, resume)

            message_api.send(sender=applicant_email,
                             recipient=job_post.contact_email,
                             subject=EmailTemplateManager.generate_email_subject(job_post),
                             body=job_form.cleaned_data['email_body'],
                             filename=resume.name,
                             attachment=resume.file)

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
