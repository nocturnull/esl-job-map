
from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.simple_tag
def build_info_html(job_post, user) -> str:
    return mark_safe(job_post.build_html_content(user))


@register.simple_tag
def has_applied(job_post, user) -> int:
    return 1 if job_post.has_applicant_applied(user) else 0
