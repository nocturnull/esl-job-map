# employment/views/job_seeking.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.db.models import F
from django.shortcuts import render, reverse

from djangomailgun.message.api import MessageApi
from cloud.file_manager import FileManager
from account.models.resume import Resume
from ..models import JobPost, JobApplication
from ..forms.recruitment import ApplyToJobForm
from ..email.template_manager import TemplateManager as EmailTemplateManager
from ..managers.apply_manager import ApplyManager


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
        request.session['referring_map_url'] = request.META['HTTP_REFERER']

        applied, application = job_post.has_applicant_applied(request.user)
        if applied:
            template = 'teacher/application_applied.html'

        return render(request,
                      template,
                      {
                          'referring_map_url': request.session['referring_map_url'],
                          'job_post': job_post,
                          'job_form': job_form
                      })

    def post(self, request, job_post_id):
        job_post = JobPost.objects.get(pk=job_post_id)
        job_form = ApplyToJobForm(request.POST, request.FILES)
        referer = request.session.get('referring_map_url', reverse('home'))
        message_api = MessageApi()
        file_manager = FileManager()

        if job_form.is_valid():
            applicant_email = job_form.cleaned_data['contact_email']
            use_existing_resume = job_form.cleaned_data['use_existing_resume']

            kwargs = {
                'job_post': job_post,
                'contact_email': applicant_email
            }

            # Attempt to use an existing resume if opted in.
            if request.user.is_authenticated:
                kwargs['site_user'] = request.user
                if use_existing_resume and request.user.teacher.has_resume:
                    kwargs['resume'] = request.user.teacher.resume

            # Make a new resume that is for this application only if needed.
            resume = job_form.cleaned_data.get('resume', None)
            if resume is not None and not use_existing_resume:
                new_resume = Resume.create_resume(filename=resume.name)
                file_manager.upload_file(new_resume.storage_path, resume)
                kwargs['resume'] = new_resume
            elif resume is None and not request.user.is_authenticated:
                return render(request,
                              self.template_name,
                              {
                                  'job_post': job_post,
                                  'job_form': job_form,
                                  'resume_error': True
                              })

            application = JobApplication.create_application(**kwargs)

            message_api.send(recipient=job_post.contact_email,
                             subject=EmailTemplateManager.generate_email_subject(job_post),
                             body=EmailTemplateManager.append_resume_to_body(
                                 job_form.cleaned_data['email_body'], application
                             ),
                             cc=applicant_email)

            return render(request,
                          'teacher/application_success.html',
                          {
                              'referring_map_url': referer,
                              'success_text': ApplyManager.resolve_success_text(referer),
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
        return JobApplication.objects.filter(site_user=self.request.user).order_by(F('created_at').desc())
