
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.views.generic import View

from ..delegates.order import OrderDelegate


class OrderLookup(LoginRequiredMixin, View):

    def get(self, request, code='', *args, **kwargs):
        """
        Lookup an order via it's code.

        :param request:
        :param code:
        :param args:
        :param kwargs:
        :return:
        """
        order = OrderDelegate.lookup(request.user, code)
        body = 'Invalid order code'
        if order is not None:
            body = order.summary

        return HttpResponse(body)

