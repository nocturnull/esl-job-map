# cloud/templatetags.py

import os

from django import template

from ..settings import AWS_CDN_BASE_LINK

register = template.Library()


@register.simple_tag
def cdn_image(path):
    host = '/'
    if os.environ.get('ESLJOBMAP_LOAD_REMOTE', None) is not None:
        host = AWS_CDN_BASE_LINK
    return host + 'static/images/' + path
