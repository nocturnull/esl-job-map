# blanket/templatetags/agent.py

from django import template

register = template.Library()


@register.filter
def is_ie(request) -> bool:
    browser = request.user_agent.browser.family
    print(browser)
    try:
        return browser.index('MSIE ') > 0
    except ValueError:
        try:
            browser.index('Trident/') > 0
        except ValueError:
            pass

    return False
