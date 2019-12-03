"""esljobmap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from esljobmap.views import ServiceDownView, Custom404

# lazy af way of catching everything, regex wasn't working for shit....
urlpatterns = [
    path('', ServiceDownView.as_view(), name='home'),
    path(r'<a>/', ServiceDownView.as_view()),
    path(r'<a>/<b>/', ServiceDownView.as_view()),
    path(r'<a>/<b>/<c>/', ServiceDownView.as_view()),
    path(r'<a>/<b>/<c>/<d>/', ServiceDownView.as_view()),
    path(r'<a>/<b>/<c>/<d>/<e>/', ServiceDownView.as_view()),
    path(r'<a>/<b>/<c>/<d>/<e>/<f>/', ServiceDownView.as_view()),
    path(r'<a>/<b>/<c>/<d>/<e>/<f>/<g>/', ServiceDownView.as_view()),
    path(r'<a>/<b>/<c>/<d>/<e>/<f>/<g>/<h>/', ServiceDownView.as_view()),
    path(r'<a>/<b>/<c>/<d>/<e>/<f>/<g>/<h>/<i>', ServiceDownView.as_view()),
    # path('kocotutor/', admin.site.urls),
    # path('korea/about/', include('about.urls')),
    # path('korea/account/', include('account.urls')),
    # path('korea/account/', include('django.contrib.auth.urls')),
    # path('korea/employment/', include('employment.urls')),
    # path('korea/job-credit/', include('job_credit.urls')),
    # path('korea/payment/', include('payment.urls')),
    # path('api/', include('task.urls'))
]

handler404 = Custom404.as_view()
