# account/decorators.py

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def recruiter_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    decor = user_passes_test(
        lambda u: u.is_active and u.is_recruiter,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        return decor(function)
    return decor
