# job_credit/views/index.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render

from ..forms.purchase import CreditPurchaseForm


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'job_credit/index.html'

    def get(self, request, *args, **kwargs):
        tab = request.GET.get('tab', 1)
        return render(request, self.template_name, {
            'tab': int(tab),
            'form': CreditPurchaseForm,
            'history': request.user.credit_history.all()
        })

    def post(self, request, *args, **kwargs):
        form = CreditPurchaseForm(request.POST)

        if form.is_valid():
            print('form is valid, make payment')
            pass

        return render(request, self.template_name, {
            'tab': 1,
            'form': form,
            'history': request.user.credit_history.all()
        })
