
from django.utils.html import escapejs
from django import template

from cloud.templatetags.remote import cdn_image

register = template.Library()


@register.simple_tag
def build_info_html(job_post, user) -> str:
    return escapejs(job_post.build_html_content(user))


@register.simple_tag
def resolve_koco_image(job_post) -> str:
    if job_post.is_full_time:
        return cdn_image('koco-man/blue-80x80.png')
    return cdn_image('koco-man/orange-80x80.png')


@register.simple_tag
def has_applied(job_post, user) -> int:
    applied, application = job_post.has_applicant_applied(user)
    return 1 if applied else 0


@register.simple_tag
def is_disinterested(job_post, user) -> int:
    return 1 if job_post.not_interested(user) else 0


@register.simple_tag
def is_job_poster(job_post, user) -> int:
    return 1 if job_post.is_job_poster(user) else 0
