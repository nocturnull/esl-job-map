# blanket/templatetags/format.py

from django import template

register = template.Library()


@register.filter
def trunc(value):
    if len(value) > 60:
        return value[:59] + '<span data-tooltip title="{}">...</span>'.format(value)
    return value
