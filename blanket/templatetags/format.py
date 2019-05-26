# blanket/templatetags/format.py

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def trunc(label, value):
    if (len(label) + len(value)) > 75:
        return mark_safe(value[:75] + '<span class="flowcard-tooltip" data-tooltip title="{}">...</span>'.format(value))
    return value
