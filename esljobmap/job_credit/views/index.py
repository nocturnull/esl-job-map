# job_credit/views/index.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'job_credit/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'history': request.user.credit_history.all()
        })
