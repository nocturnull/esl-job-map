# esljobmap/views.py

from django.views.generic import TemplateView

from employment.settings import FULL_TIME_JOB_DAYS_VALID, PART_TIME_JOB_DAYS_VALID


class HomeView(TemplateView):
    template_name = 'home.html'
    extra_context = {
        'full_time_job_days_valid': FULL_TIME_JOB_DAYS_VALID,
        'part_timejob_days_valid': PART_TIME_JOB_DAYS_VALID
    }


class Custom404(TemplateView):
    template_name = 'errors/404.html'
