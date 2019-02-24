# task/views/generic.py

from django.views.generic import View

from task.mixins.auth import RequestAuthenticationMixin


class ApiView(RequestAuthenticationMixin, View):
    """Base API View"""
    pass
