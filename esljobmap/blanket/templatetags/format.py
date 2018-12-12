# blanket/templatetags/format.py

from django import template

register = template.Library()


@register.filter
def trunc(value):
    if len(value) > 10:
        return value[:9] + '<span data-tooltip title="{}">...</span>'.format(value)
    return value
