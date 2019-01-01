# blanket/templatetags/format.py

from django import template

register = template.Library()


@register.filter
def classify(path):
    if 'full-time' in path or 'part-time' in path:
        return 'gmap'
    return 'zilch'
