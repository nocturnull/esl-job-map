# task/resources/email/template_manager.py

from django.shortcuts import reverse

from employment.models import JobPost

from task.lib.security import JwtAuthentication
from .scheme import *


class TemplateManager:
    """Manager that aides in building the email body for job post expiry notifications."""

    @staticmethod
    def generate_email_subject(job_post: JobPost) -> str:
        """
        The main API that creates the email subject.

        :param job_post:
        :return:
        """
        return SUBJECT_BASE_SCHEME.format(title=job_post.title)

    @classmethod
    def generate_email_body(cls, job_post: JobPost, request) -> str:
        """
        The main API that creates the email body using a template and the users submitted info.

        :param job_post:
        :param request:
        :return:
        """
        exclusive_info_section = cls._generate_exclusive_info_section(job_post)
        applicants_notice_section = cls._generate_applicants_section(job_post, request)
        opt_out_link = cls._generate_opt_out_email_link(job_post.contact_email, request)

        return BODY_BASE_SCHEME.format(
            contact_name=job_post.contact_name,
            title=job_post.title,
            exclusive_info_section=exclusive_info_section,
            schedule=job_post.schedule,
            class_type=job_post.class_type,
            other_requirements=job_post.other_requirements,
            address=job_post.address,
            applicants_notice_section=applicants_notice_section,
            email_opt_out_link=opt_out_link
        )

    @classmethod
    def _generate_exclusive_info_section(cls, job_post: JobPost) -> str:
        """
        Generates a part of the template that is exclusive to the type of the job.

        :param job_post:
        :return:
        """
        if job_post.is_full_time:
            return FULL_TIME_EXCLUSIVE_SCHEME.format(
                salary=job_post.salary,
                benefits=job_post.benefits
            )
        return PART_TIME_EXCLUSIVE_SCHEME.format(pay_rate=job_post.pay_rate)

    @classmethod
    def _generate_applicants_section(cls, job_post: JobPost, request) -> str:
        """
        Generate a part of the template that depends on the number of applicants and job type.

        :param job_post:
        :param request:
        :return:
        """
        applicant_count = job_post.num_applicants(job_post.site_user)

        if applicant_count > 0:
            return HAS_APPLICANTS_SCHEME.format(
                applicants_job_post_url=request.build_absolute_uri(job_post.applicants_link),
                num_applicants=applicant_count,
                repost_job_post_url=request.build_absolute_uri(job_post.repost_link)
            )
        return NO_APPLICANTS_SCHEME.format(
            repost_job_post_url=request.build_absolute_uri(job_post.repost_link),
            create_job_post_url=request.build_absolute_uri(job_post.recruiter_create_job_link)
        )

    @classmethod
    def _generate_opt_out_email_link(cls, email: str, request) -> str:
        """
        Generate the expired job notification opt out email link.

        :param email:
        :param request:
        :return:
        """
        return '{url}?tok={token}'.format(
            url=request.build_absolute_uri(reverse('recruiter_opt_out_expired_notif')),
            token=JwtAuthentication.encode(email, True).decode('utf-8')
        )
