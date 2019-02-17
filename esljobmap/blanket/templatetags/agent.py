# blanket/templatetags/agent.py

from django import template

register = template.Library()


@register.filter
def is_ie(request) -> bool:
    browser = request.user_agent.browser.family
    try:
        return browser.index('IE') >= 0
    except ValueError:
        pass

    return False
