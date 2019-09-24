# account/views/recruiter.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages

from ..forms.recruiter import RecruiterCreationForm, RecruiterUpdateForm, AutofillOptionsForm
from ..helpers.recruiter import RecruiterHelper

from payment.delegates.subscription import SubscriptionDelegate
from task.lib.security import JwtAuthentication


class RecruiterRegister(CreateView):
    form_class = RecruiterCreationForm
    template_name = 'registration/register/recruiter.html'
    extra_context = {
        'mtitle': 'Register as a Recruiter on ESL Job Map',
        'mdescription': 'Register as a job poster to post jobs on ESL Job Map'
                        ' and find the teacher right for you, quickly!'
    }

    def get_context_data(self, **kwargs):
        kwargs['role'] = 'recruiter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('account_profile')


class RecruiterProfile(LoginRequiredMixin, TemplateView):
    template_name = 'profile/recruiter/index.html'

    def get(self, request, **kwargs):
        bill_date = SubscriptionDelegate.get_bill_date(request.user)
        next_bill_date = ''
        if bill_date is not None:
            next_bill_date = bill_date.strftime('%b %d %Y')

        return render(
            request,
            self.template_name,
            {
                'tab': int(request.GET.get('tab', 1)),
                'next_bill_date': next_bill_date,
                'user_form': RecruiterUpdateForm(instance=request.user),
                'autofill_form': AutofillOptionsForm(instance=request.user.autofill),
                'profile_url': reverse_lazy('recruiter_profile_edit'),
                'autofill_url': reverse_lazy('recruiter_autofill_options'),
                'notice': 'This information will be used to automatically fill in your job fields'
            }
        )


class EditRecruiterProfile(LoginRequiredMixin, TemplateView):
    template_name = 'profile/recruiter/index.html'
    success_url = reverse_lazy('recruiter_profile')

    def post(self, request, **kwargs):
        form = RecruiterUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved!')

        return render(
            request,
            self.template_name,
            {
                'tab': 1,
                'user_form': form,
                'autofill_form': AutofillOptionsForm(instance=request.user.autofill),
                'profile_url': reverse_lazy('recruiter_profile_edit'),
                'autofill_url': reverse_lazy('recruiter_autofill_options'),
                'notice': 'This information will be used to automatically fill in your job fields'
            }
        )


class EditAutofillOptions(LoginRequiredMixin, TemplateView):
    template_name = 'profile/recruiter/index.html'
    success_url = reverse_lazy('recruiter_profile')

    def post(self, request, **kwargs):
        form = AutofillOptionsForm(request.POST, instance=request.user.autofill)

        if form.is_valid():
            options = form.save(False)
            options.site_user = request.user
            options.save()
            messages.success(request, 'Changes saved!')

        return render(
            request,
            self.template_name,
            {
                'tab': 2,
                'user_form': RecruiterUpdateForm(instance=request.user),
                'autofill_form': form,
                'profile_url': reverse_lazy('recruiter_profile_edit'),
                'autofill_url': reverse_lazy('recruiter_autofill_options'),
                'notice': 'This information will be used to automatically fill in your job fields'
            }
        )


class OptOutExpiredPostNotifications(TemplateView):
    template_name = 'account/expired_post_email_opt_out_notice.html'

    def get(self, request, *args, **kwargs):
        token = request.GET.get('tok', '')
        payload = JwtAuthentication.decode(token)
        status = RecruiterHelper.opt_out_of_expired_post_emails(payload)

        return render(
            request,
            self.template_name,
            {
                'status': status
            }
        )
