# job_credit/urls.py

from django.urls import path

from .views.index import Index


urlpatterns = [
    path('', Index.as_view(), name='job_credit')
]
