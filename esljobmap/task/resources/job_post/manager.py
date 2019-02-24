# task/resources/job_post/manager.py

from djangomailgun.message.api import MessageApi

from ..email.template_manager import TemplateManager as EmailTemplateManager
from .scavenger import JobPostScavenger


class JobPostManager:
    """Background task management interface for job posts"""

    @classmethod
    def send_expiry_emails(cls) -> int:
        """
        Fetch and process the job posts.

        :return:
        """
        jobs = JobPostScavenger.get_expired_full_time()
        jobs.extend(JobPostScavenger.get_expired_part_time())
        emails_sent = cls._send_emails_and_tag_jobs(jobs)

        return emails_sent

    @classmethod
    def _send_emails_and_tag_jobs(cls, jobs: list) -> int:
        """
        Sends emails and marks the jobs as 'email sent' at the same time.

        :param jobs:
        :return:
        """
        message_api = MessageApi()
        for job_post in jobs:
            html_body = EmailTemplateManager.generate_email_body(job_post)
            message_api.send(recipient=job_post.contact_email,
                             subject=EmailTemplateManager.generate_email_subject(job_post),
                             body=html_body,
                             html=html_body)
            job_post.expiry_notice_sent = True
            job_post.save()

        return len(jobs)
