from django import template

register = template.Library()


@register.simple_tag
def is_recruiter(request) -> bool:
    if request is not None:
        return request.user.is_authenticated and request.user.is_recruiter
    return False


@register.simple_tag
def visa_conditions_class(user) -> str:
    return '' if user.teacher.is_e1e2_holder else 'invisible'
