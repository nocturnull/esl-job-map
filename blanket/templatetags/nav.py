# blanket/templatetags/nav.py

from django.urls import reverse, NoReverseMatch
from django import template

register = template.Library()


@register.simple_tag
def menu_class(request, named_url, *args):
    current_path = request.path_info
    mclass = 'dormant'

    try:
        item_url = reverse(named_url, args=args)

        if current_path == item_url:
            mclass = 'active'

        return mclass

    except NoReverseMatch:
        pass

    if named_url in current_path:
        mclass = 'active'

    return mclass


@register.simple_tag
def map_url(user, uri, location=''):
    rargs = [location] if len(location) > 0 else []
    url = reverse(uri, args=rargs)
    if user.is_authenticated and user.is_recruiter:
        url += '#postAnchor'

    return url


@register.simple_tag
def full_time_label(user):
    if user.is_authenticated and user.is_recruiter:
        return 'Post Full-Time'
    return 'Full-Time Map'


@register.simple_tag
def part_time_label(user):
    if user.is_authenticated and user.is_recruiter:
        return 'Post Part-Time'
    return 'Part-Time Map'
