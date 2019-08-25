
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse

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
        if order is None:
            return JsonResponse({'error': 'Invalid order code'})

        return JsonResponse({
            'detailedInfo': order.detailed_info,
            'priceInfo': order.price_info,
            'error': ''
        })

