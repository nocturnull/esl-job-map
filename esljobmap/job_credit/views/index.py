# job_credit/views/index.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'job_credit/index.html'

    def get(self, request, *args, **kwargs):
        tab = request.GET.get('tab', 1)
        return render(request, self.template_name, {
            'tab': int(tab),
            'history': request.user.credit_history.all()
        })
