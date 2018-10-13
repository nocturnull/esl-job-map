# employment/views/job_seeking.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.shortcuts import render

from djangomailgun.message.api import MessageApi
from cloud.file_manager import FileManager
from ..models import JobPost, JobApplication
from ..forms.recruitment import ApplyToJobForm
from ..email.template_manager import TemplateManager as EmailTemplateManager


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
            use_existing_resume = job_form.cleaned_data['use_existing_resume']
            resume = None

            kwargs = {
                'job_post': job_post,
                'contact_email': applicant_email
            }
            if request.user.is_authenticated:
                kwargs['site_user'] = request.user
            if use_existing_resume:
                kwargs['use_existing_resume'] = True
            else:
                resume = job_form.cleaned_data.get('resume', None)
                kwargs['filename'] = resume.name

            application = JobApplication.create_job(**kwargs)
            if resume is not None:
                file_manager.upload_file(application.storage_path, resume)

            message_api.send(sender=applicant_email,
                             recipient=job_post.contact_email,
                             subject=EmailTemplateManager.generate_email_subject(job_post),
                             body=EmailTemplateManager.append_resume_to_body(
                                 job_form.cleaned_data['email_body'], application
                             ))

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


class ListApplications(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = 'teacher/application_list.html'

    def get_queryset(self):
        return JobApplication.objects.filter(site_user=self.request.user)
