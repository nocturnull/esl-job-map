# employment/managers/apply_manager.py

from djangomailgun.message.api import MessageApi

from ..email.template_manager import TemplateManager as EmailTemplateManager
from ..forms.applicant import ApplyToJobForm
from ..models import JobPost, JobApplication

from cloud.file_manager import FileManager
from account.models import Resume, Photo


class ApplyManager:
    """Manager for job application related tasks"""

    @staticmethod
    def track_referer(request):
        """
        After an application is submitted, we need to take the user back to where they came from.

        :param request:
        :return:
        """
        try:
            request.session['referring_map_url'] = request.META['HTTP_REFERER']
        except KeyError:
            pass

    @staticmethod
    def track_application_info(request, application: JobApplication):
        """
        Track application to be used in the signup form.

        :param request:
        :param application:
        :return:
        """
        request.session['recent_application'] = application.id
        request.session['recent_applicant_email'] = application.contact_email

    @staticmethod
    def untrack_application_info(request):
        """
        Remove application once used.

        :param request:
        :return:
        """
        try:
            del request.session['recent_application']
            del request.session['recent_applicant_email']
        except KeyError:
            pass

    @staticmethod
    def save_resume(user, resume, **kwargs) -> dict:
        """
        Use an existing resume for logged in users or grab one from the form.

        :param user:
        :param resume:
        :param kwargs:
        :return:
        """
        # Attempt to use an existing resume if possible.
        if user.is_authenticated:
            kwargs['site_user'] = user
            if user.teacher.has_resume and resume is None:
                kwargs['resume'] = user.teacher.resume

        # Make a new resume that is for this application only if needed.
        if resume is not None:
            file_manager = FileManager()
            new_resume = Resume.create_resume(filename=resume.name)
            file_manager.upload_file(new_resume.storage_path, resume)
            kwargs['resume'] = new_resume

        return kwargs

    @staticmethod
    def save_photo(user, photo, **kwargs) -> dict:
        """
        Use an existing photo for logged in users or grab one from the form.

        :param user:
        :param photo:
        :param kwargs:
        :return:
        """
        # Attempt to use an existing photo if possible
        if user.is_authenticated:
            if user.teacher.has_photo and photo is None:
                kwargs['photo'] = user.teacher.photo

        # Make a new photo that is for this application only if needed.
        if photo is not None:
            file_manager = FileManager()
            new_photo = Photo.create_photo(filename=photo.name)
            file_manager.upload_file(new_photo.storage_path, photo)
            kwargs['photo'] = new_photo

        return kwargs

    @staticmethod
    def email_relevant_parties(job_post: JobPost, job_form: ApplyToJobForm, application: JobApplication, user, email):
        """
        Either the recruiter or the applicant can opt out of emails.
        Only email those who have opted in to email notifications.

        :param job_post:
        :param job_form:
        :param application:
        :param user:
        :param email:
        :return:
        """
        recruiter = job_post.site_user

        # Check if recruiter allowed emails and or if the user is banned.
        send_email = True
        if user.is_authenticated:
            send_email = not user.is_banned

        if not recruiter.opted_out_of_emails and send_email:
            message_api = MessageApi()
            applicant_email = email

            # If the user is logged in, check if they opted out.
            if user.is_authenticated:
                if user.opted_out_of_emails:
                    applicant_email = None

            message_api.send(recipient=job_post.contact_email,
                             subject=EmailTemplateManager.generate_email_subject(job_post),
                             body=EmailTemplateManager.append_relevant_files(
                                 job_form.cleaned_data['email_body'], application
                             ),
                             cc=applicant_email)

    @staticmethod
    def resolve_success_text(referer) -> str:
        """
        Show the relevant message when the user has finished applying.

        :param referer:
        :return: str
        """
        if 'full-time/seoul' in referer:
            text = 'Apply to more Full-Time jobs in Seoul'
        elif 'full-time/busan' in referer:
            text = 'Apply to more Full-Time jobs in Busan'
        elif 'full-time' in referer:
            text = 'Apply to more Full-Time jobs'
        elif 'part-time/seoul' in referer:
            text = 'Apply to more Part-Time jobs in Seoul'
        elif 'part-time/busan' in referer:
            text = 'Apply to more Part-Time jobs in Busan'
        else:
            text = 'Apply to more Part-Time jobs'

        return text
