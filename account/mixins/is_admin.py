
from django.http.response import HttpResponseForbidden


class IsAdminMixin:
    """Mixin to check job poster permissions."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()
