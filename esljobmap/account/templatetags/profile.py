from django import template

register = template.Library()


@register.simple_tag
def is_recruiter(request) -> bool:
    if request is not None:
        try:
            return request.user.is_authenticated and request.user.is_recruiter
        except AttributeError:
            pass

    return False
