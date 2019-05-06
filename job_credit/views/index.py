# job_credit/views/index.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render

from ..forms.purchase import CreditPurchaseForm
from ..form_helpers.purchase import PurchaseHelper

from payment.manager import PaymentManager


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
        error_message = None

        if form.is_valid():
            purchase_helper = PurchaseHelper(form)
            num_credits = purchase_helper.get_credits()
            if num_credits > 0:
                PaymentManager.charge(
                    job_credits=num_credits,
                    total_price=purchase_helper.calculate_total(),
                    user=request.user,
                    stripe_token=request.POST.get('stripeToken')
                )
                return render(request, 'job_credit/success.html', {'job_credits': num_credits})
            else:
                error_message = 'Please specify a desired quantity.'

        return render(request, self.template_name, {
            'tab': 1,
            'form': form,
            'history': request.user.credit_history.all(),
            'error_message': error_message
        })
