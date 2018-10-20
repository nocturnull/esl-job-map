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
