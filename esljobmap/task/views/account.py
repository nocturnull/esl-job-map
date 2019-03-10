# task/views/job_post.py

from django.http.response import HttpResponse

from account.models import SiteUser
from .generic import ApiView


class UpdateNames(ApiView):
    """View for sending job post expiry notifications."""

    def get(self, request, *args, **kwargs):
        """
        curl -i -H 'Authorization: {username} {token}' http://{path}/task/account/update-names

        :return:
        """
        users = SiteUser.objects.extra(where=["length(first_name) > 0"]).all()
        c = 0
        for u in users:
            if len(u.last_name) > 0:
                u.name = u.first_name + ' ' + u.last_name
            else:
                u.name = u.first_name
            u.save()
            c += 1

        return HttpResponse('{}\n'.format(c))
