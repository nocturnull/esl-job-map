# task/resources/job_post/manager.py

from djangomailgun.message.api import MessageApi

from ..email.template_manager import TemplateManager as EmailTemplateManager
from .scavenger import JobPostScavenger


class JobPostManager:
    """Background task management interface for job posts"""

    @classmethod
    def send_expiry_emails(cls, request) -> int:
        """
        Fetch and process the job posts.

        :return:
        """
        jobs = JobPostScavenger.get_expired_full_time()
        jobs.extend(JobPostScavenger.get_expired_part_time())
        emails_sent = cls._send_emails_and_tag_jobs(jobs, request)

        return emails_sent

    @classmethod
    def update_posted_dates(cls) -> int:
        """
        Manually update existing data posted at dates.

        :return:
        """
        jobs = JobPostScavenger.all()
        amount = 0

        for j in jobs:
            if j.reposted_at is None:
                pat = j.created_at
            else:
                pat = j.reposted_at
            j.posted_at = pat
            j.save()
            amount += 1
        return amount

    @classmethod
    def _send_emails_and_tag_jobs(cls, jobs: list, request) -> int:
        """
        Sends emails and marks the jobs as 'email sent' at the same time.

        :param jobs:
        :param request:
        :return:
        """
        message_api = MessageApi()
        limit = 0
        for job_post in jobs:
            if limit < 5:
                html_body = EmailTemplateManager.generate_email_body(job_post, request)
                message_api.send(recipient=job_post.site_user_email,
                                 subject=EmailTemplateManager.generate_email_subject(job_post),
                                 body=html_body,
                                 html=html_body)
                job_post.expiry_notice_sent = True
                job_post.save()
            else:
                break
            limit += 1

        return len(jobs)
