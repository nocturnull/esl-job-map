# employment/views/job_seeking.py

from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import login
from django.db.models import F

from account.forms.applicant import ApplicantCreationForm

from ..models import JobPost, JobApplication
from ..forms.applicant import ApplyToJobForm
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
        ApplyManager.track_referer(request)

        applied, application = job_post.has_applicant_applied(request.user)
        if applied:
            template = 'teacher/application_applied.html'

        return render(request,
                      template,
                      {
                          'referring_map_url': request.session['referring_map_url'],
                          'job_post': job_post,
                          'recruiter': job_post.site_user,
                          'job_form': job_form
                      })

    def post(self, request, job_post_id):
        job_post = JobPost.objects.get(pk=job_post_id)
        job_form = ApplyToJobForm(request.POST, request.FILES)
        referer = request.session.get('referring_map_url', reverse('home'))

        if job_form.is_valid():
            applicant_email = job_form.cleaned_data['contact_email']
            resume = job_form.cleaned_data.get('resume', None)
            photo = job_form.cleaned_data.get('photo', None)

            kwargs = {
                'job_post': job_post,
                'contact_email': applicant_email,
                'cover_letter': job_form.cleaned_data['email_body']
            }

            # Figure out which resume to use.
            kwargs = ApplyManager.save_resume(request.user, resume, **kwargs)

            # If the user did not upload a resume and has no resume on file, show an error.
            if 'resume' not in kwargs:
                return render(request,
                              self.template_name,
                              {
                                  'job_post': job_post,
                                  'job_form': job_form,
                                  'resume_error': True
                              })

            # Figure out which photo to use.
            kwargs = ApplyManager.save_photo(request.user, photo, **kwargs)

            # Save the application info.
            application = JobApplication.create_application(**kwargs)

            # Dispatch email.
            ApplyManager.email_relevant_parties(job_post, job_form, application, request.user, applicant_email)

            # Inform the user.
            if self.request.user.is_authenticated:
                return render(request,
                              'teacher/application_success.html',
                              {
                                  'referring_map_url': referer,
                                  'success_text': ApplyManager.resolve_success_text(referer),
                              })
            else:
                ApplyManager.track_application_info(request, application)
                return redirect(reverse('employment_applied_signup'))
        else:
            return render(request,
                          self.template_name,
                          {
                              'job_post': job_post,
                              'job_form': job_form
                          })


class RegistrationAfterApplying(TemplateView):
    template_name = 'registration/signup/application_submitted.html'
    extra_context = {
        'mtitle': 'Register as a Teacher on ESL Job Map',
        'mdescription': 'Creating an account will allow you to automatically attach your resume, '
                        'fill in information on your cover letter and track jobs you have applied to.',
        'role': 'teacher'
    }

    def get(self, request, *args, **kwargs):
        applicant_email = request.session.get('recent_applicant_email')

        # Set default email for the signup form.
        form = ApplicantCreationForm()
        form.fields['email'].initial = applicant_email
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ApplicantCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Link the users new account to their recent application.
            application_id = request.session.get('recent_application')
            if application_id is not None:
                try:
                    application = JobApplication.objects.get(id=application_id)
                    application.site_user = user
                    application.save()

                    # Link the applications resume and photo to the users account.
                    user.teacher.resume = application.resume
                    if application.photo:
                        user.teacher.photo = application.photo
                    user.teacher.save()
                    ApplyManager.untrack_application_info(request)
                except JobApplication.DoesNotExist:
                    pass

                # Log them in and redirect to their applications.
                login(self.request, user)
                return redirect('employment_applications')
        return render(request, self.template_name, {'form': form})


class ListApplications(LoginRequiredMixin, ListView):
    model = JobApplication
    template_name = 'teacher/application_list.html'

    def get_queryset(self):
        return JobApplication.objects.filter(site_user=self.request.user).order_by(F('created_at').desc())
