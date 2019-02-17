# employment/forms/recruiter.py

from datetime import datetime

from django import forms

from employment.models.recruitment import JobPost

from .create import CreateJobForm


class EditFullTimeJobForm(CreateJobForm):
    salary = forms.CharField(label='Salary',
                             widget=forms.TextInput(attrs={'placeholder': 'Ex) Negotiable'}),
                             required=True)
    benefits = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ex) Accommodation provided'}),
                               required=False,
                               empty_value='')

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'contact_name', 'contact_email',
                  'contact_number', 'schedule', 'other_requirements', 'salary', 'benefits']


class EditPartTimeJobForm(CreateJobForm):
    pay_rate = forms.CharField(label='Pay Rate',
                               widget=forms.TextInput(attrs={'placeholder': 'Ex) 45,000 per hour'}))

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'contact_name', 'contact_email',
                  'contact_number', 'schedule', 'other_requirements', 'pay_rate']


class CloseJobForm(forms.ModelForm):
    """Form for recruiters to hide their job post from the public."""
    is_visible = forms.HiddenInput()

    def save(self, commit=True):
        """
        Hook into the save to update the visibility field.

        :param commit:
        :return:
        """

        self.instance.is_visible = False

        return super(CloseJobForm, self).save(commit=commit)

    class Meta:
        model = JobPost
        fields = ['is_visible']


class RestoreJobForm(forms.ModelForm):
    """Form for recruiters to restore their job post for the public to see."""
    is_visible = forms.HiddenInput()

    def save(self, commit=True):
        """
        Hook into the save to update the visibility field.

        :param commit:
        :return:
        """

        self.instance.is_visible = True

        return super(RestoreJobForm, self).save(commit=commit)

    class Meta:
        model = JobPost
        fields = ['is_visible']


class RepostJobForm(forms.Form):
    """Form for recruiters to repost their job post for the public to see."""
    confirm = forms.HiddenInput()

    class Meta:
        fields = ['confirm']


