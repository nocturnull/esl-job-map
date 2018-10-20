# cloud/templatetags.py
from django import template

register = template.Library()


@register.simple_tag
def cdn_image(path):
    return '/static/images/' + path
