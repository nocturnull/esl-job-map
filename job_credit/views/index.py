# job_credit/views/index.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.shortcuts import render

from ..forms.purchase import CreditPurchaseForm
from ..form_helpers.purchase import PurchaseHelper

from payment.manager import PaymentManager
from payment.settings import STRIPE_PUBLISHABLE_KEY


class Index(LoginRequiredMixin, ListView):
    template_name = 'job_credit/index.html'

    def get_queryset(self):
        return self.request.user.credit_history.order_by('-updated_at').all()

    def get(self, request, *args, **kwargs):
        tab = request.GET.get('tab', 1)
        return render(request, self.template_name, {
            'publishable_key': STRIPE_PUBLISHABLE_KEY,
            'tab': int(tab),
            'form': CreditPurchaseForm,
            'history': self.get_queryset()
        })

    def post(self, request, *args, **kwargs):
        form = CreditPurchaseForm(request.POST)
        error_message = None

        if form.is_valid():
            purchase_helper = PurchaseHelper(form)
            num_credits = purchase_helper.get_credits()
            order_code = form.cleaned_data.get('order_code')

            if order_code:
                status = PaymentManager.subscribe(
                    order_code=order_code,
                    user=request.user,
                    stripe_token=request.POST.get('stripeToken')
                )
                if status:
                    return render(request, 'job_credit/success/subscription.html')
                else:
                    error_message = 'Unable to place subscription order, contact us for help.'

            elif num_credits > 0:
                status = PaymentManager.charge(
                    job_credits=num_credits,
                    total_price=purchase_helper.calculate_total(),
                    user=request.user,
                    stripe_token=request.POST.get('stripeToken')
                )
                if status:
                    return render(request, 'job_credit/success/credit_purchase.html', {'job_credits': num_credits})
                else:
                    error_message = 'An error occurred, please contact us for assistance.'
            else:
                error_message = 'Please specify a desired quantity or order code.'

        return render(request, self.template_name, {
            'publishable_key': STRIPE_PUBLISHABLE_KEY,
            'tab': 1,
            'form': form,
            'history': self.get_queryset(),
            'error_message': error_message
        })
