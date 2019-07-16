# esljobmap/views.py

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'


class Custom404(TemplateView):
    template_name = 'errors/404.html'
