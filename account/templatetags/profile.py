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


@register.simple_tag
def credit_text(request, text) -> str:
    if request is not None:
        try:
            if request.user.is_authenticated and request.user.is_recruiter and request.user.has_subscription:
                return ''
        except AttributeError:
            pass

    return text
