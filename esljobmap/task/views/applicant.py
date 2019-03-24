# task/views/applicant.py

from djangomailgun.message.api import MessageApi
from django.http.response import HttpResponse

from employment.email.template_manager import TemplateManager as EmailTemplateManager
from employment.models import JobPost, JobApplication
from account.models import SiteUser
from .generic import ApiView


class SendApplicationEmails(ApiView):

    def post(self, request, *args, **kwargs):
        """
        curl -i -H 'Authorization: {username} {token}' http://{path}/api/employment/send-application-emails

        :return:
        """
        user = SiteUser.objects.get(email=request.POST['email'])
        applications = user.job_applications.filter(id__in=[468, 463, 464, 465, 466, 467, 469])
        application_ids = ''
        for app in applications:
            job_post = app.job_post
            cover_letter = app.cover_letter
            application_ids += str(app.id) + ','

            # Dispatch email.
            self._send_email(cover_letter, job_post, app, user)

        return HttpResponse('{}\n'.format(application_ids))

    @classmethod
    def _send_email(cls, email_body: str, job_post: JobPost, application: JobApplication, user: SiteUser):
        recruiter = job_post.site_user

        # Check if recruiter allowed emails and or if the user is banned.
        send_email = not user.is_banned

        if not recruiter.opted_out_of_emails and send_email:
            message_api = MessageApi()
            applicant_email = user.email

            # Check if they opted out.
            if user.opted_out_of_emails:
                applicant_email = None

            message_api.send(recipient=recruiter.email,
                             subject=EmailTemplateManager.generate_email_subject(job_post),
                             body=EmailTemplateManager.append_relevant_files(
                                 email_body, application
                             ),
                             cc=applicant_email
            )
