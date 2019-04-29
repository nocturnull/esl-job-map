# task/mixins/auth.py

from ..lib.security import JwtAuthentication
from ..settings import AUTH_USERNAME

from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse


class RequestAuthenticationMixin:
    """Verify that the request is authorized to access any API resource."""

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        """
        Upon request invocation, ensure the request is authorized.
        Since we are handling our own authentication we can also disable CSRF.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        payload = None
        try:
            fields = request.META['HTTP_AUTHORIZATION'].split(' ')
            if fields[0].lower() == AUTH_USERNAME:
                payload = JwtAuthentication.decode(fields[1])
        except (KeyError, IndexError):
            pass

        if payload is None:
            return HttpResponse('Unauthorized request\n', status=401)
        return super().dispatch(request, *args, **kwargs)


