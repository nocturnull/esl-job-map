# account/models/role.py

from .scheme import *
from ..models.recruitment import JobPost
from ..models.job_seeking import JobApplication
from account.models.user import SiteUser
from account.models.applicant import Teacher


class TemplateManager:
    """
    Manager that aides in building the email body for job applications.
    """

    @staticmethod
    def generate_email_subject(job_post: JobPost) -> str:
        """
        The main API that creates the email subject.

        :param job_post:
        :return:
        """
        return SUBJECT_BASE_SCHEME.format(title=job_post.title)

    @classmethod
    def generate_email_body(cls, user, job_post: JobPost) -> str:
        """
        The main API that creates the email body using a template and the users submitted info.

        :param user:
        :param job_post:
        :return:
        """
        if user.is_authenticated and user.is_teacher:
            return cls._generate_applicant_email_body(user, job_post)
        return cls._generate_anonymous_email_body(job_post)

    @classmethod
    def append_relevant_files(cls, body: str, job_application: JobApplication) -> str:
        """
        Appends any relevant files.

        :param body:
        :param job_application:
        :return:
        """
        # Append resume first.
        resume_url = job_application.resume.cdn_url
        contents = '{0}\n\nResume: {1}'.format(body, resume_url)

        if job_application.photo is not None:
            photo_url = job_application.photo.cdn_url
            contents = '{0}\n\nPhoto: {1}'.format(contents, photo_url)

        return contents

    @classmethod
    def _generate_applicant_email_body(cls, applicant: SiteUser, job_post: JobPost) -> str:
        """
        Builds the email body for applicants that have a registered account on the site.

        :param applicant:
        :param job_post:
        :return:
        """
        teacher = applicant.teacher

        return AUTHENTICATED_USER_BASE_SCHEME.format(
            recruiter_contact_name=cls._generated_to_recruiter_intro(job_post.contact_name),
            applicant_country=teacher.nice_country,
            job_post_title=job_post.title,
            exclusive_job_post_info=cls._generate_job_exclusive_template(job_post),
            job_post_schedule=job_post.schedule,
            job_post_class_type=job_post.class_type,
            job_post_other_requirements=job_post.other_requirements,
            applicant_full_name=cls._generated_to_applicant_outro(applicant),
            applicant_email=applicant.email,
            applicant_contact_number=applicant.phone_number
        )

    @classmethod
    def _generate_anonymous_email_body(cls, job_post: JobPost) -> str:
        """
        Builds the email body for applicants that are simply 'guests' to the site.

        :param recruiter:
        :return:
        """
        return ANONYMOUS_USER_BASE_SCHEME.format(
            recruiter_contact_name=cls._generated_to_recruiter_intro(job_post.contact_name)
        )

    @staticmethod
    def _generate_job_exclusive_template(job_post: JobPost) -> str:
        """
        Generates a part of the template that is exclusive to the type of job that it is.

        :param job_post:
        :return:
        """
        if job_post.is_full_time:
            return FULL_TIME_EXCLUSIVE_SCHEME.format(
                job_post_salary=job_post.salary,
                job_post_benefits=job_post.benefits
            )
        return PART_TIME_EXCLUSIVE_SCHEME.format(job_post_pay_rate=job_post.pay_rate)

    @staticmethod
    def _generated_to_recruiter_intro(recruiter: str) -> str:
        """
        Create the appropriate intro text.

        :param recruiter:
        :return:
        """
        if len(recruiter) > 0:
            return 'Dear ' + recruiter
        return 'To Whom it May Concern'

    @staticmethod
    def _generated_to_applicant_outro(applicant: SiteUser) -> str:
        """
        Create the appropriate outro text.

        :param applicant:
        :return:
        """
        if len(applicant.full_name) > 0:
            return applicant.full_name
        return 'YOUR NAME'
