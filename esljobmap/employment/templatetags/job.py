from django import template

register = template.Library()


@register.filter
def is_mod3(counter) -> bool:
    return counter % 3 == 0
