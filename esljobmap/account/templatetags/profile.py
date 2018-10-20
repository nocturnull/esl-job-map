from django import template

register = template.Library()


@register.simple_tag
def is_recruiter(request) -> bool:
    return request.user.is_authenticated and request.user.is_recruiter
