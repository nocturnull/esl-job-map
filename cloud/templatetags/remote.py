# cloud/templatetags.py

from django import template

from ..settings import *

register = template.Library()


@register.simple_tag
def cdn_image(path, secure=True):
    host = '/'
    if os.environ.get('ESLJOBMAP_LOAD_REMOTE', None) is not None:
        if secure:
            host = AWS_SECURE_CDN_BASE_LINK
        else:
            host = AWS_STANDARD_CDN_BASE_LINK
    return host + 'assets/images/' + path
