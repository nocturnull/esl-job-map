# task/views/token.py

from django.http.response import HttpResponse
from django.views.generic import View

from task.lib.security import JwtAuthentication


class GenerateToken(View):
    """Endpoint for generating access tokens."""

    def get(self, request, *args, **kwargs):
        """
        curl -i http://{path}/auth/grant

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return HttpResponse('{}\n'.format(JwtAuthentication.encode()))
