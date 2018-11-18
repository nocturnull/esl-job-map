
from django.utils.safestring import mark_safe
from django import template

from cloud.templatetags.remote import cdn_image

register = template.Library()


@register.simple_tag
def build_info_html(job_post, user) -> str:
    return mark_safe(job_post.build_html_content(user))


@register.simple_tag
def resolve_koco_image(job_post) -> str:
    if job_post.is_full_time:
        return cdn_image('koco-man/koco-blue-40x40.png')
    return cdn_image('koco-man/koco-orange-40x40.png')


@register.simple_tag
def has_applied(job_post, user) -> int:
    return 1 if job_post.has_applicant_applied(user) else 0


@register.simple_tag
def is_disinterested(job_post, user) -> int:
    return 1 if job_post.not_interested(user) else 0


@register.simple_tag
def is_job_poster(job_post, user) -> int:
    return 1 if job_post.is_job_poster(user) else 0
