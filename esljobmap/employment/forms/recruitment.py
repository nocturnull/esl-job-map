# employment/forms/recruitment.py
from django import forms
from ..models.recruitment import JobPost


class CreateJobForm(forms.ModelForm):
    """Form for recruiters to create a new job post."""
    JOB_TYPE_CHOICES = ((True, 'Full-time'), (False, 'Part-time'))

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Give a short, descriptive title!'}))
    class_type = forms.CharField(label='Class Type', widget=forms.TextInput(attrs={'placeholder': 'i.e 1:1 Business English / Speaking'}))
    contact_name = forms.CharField(label='Contact Name', widget=forms.TextInput(attrs={'placeholder': 'i.e Your name'}))
    contact_email = forms.CharField(label='Contact Email', widget=forms.TextInput(attrs={'placeholder': 'i.e name@email.com'}))
    contact_number = forms.CharField(label='Contact Number', widget=forms.TextInput(attrs={'placeholder': 'i.e 010-0000-0000'}))
    schedule = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'i.e Mon-Fri 9-6'}))
    other_requirements = forms.CharField(label='Other Requirements', widget=forms.TextInput(attrs={'placeholder': 'i.e Teaching certificate'}))
    is_full_time = forms.ChoiceField(label='Job Type',
                                     widget=forms.RadioSelect,
                                     choices=((True, 'Full-time'), (False, 'Part-time')))
    pay_rate = forms.CharField(label='Pay Rate',
                               widget=forms.TextInput(attrs={'placeholder': 'i.e 45,000 per hour'}),
                               required=False)
    salary = forms.CharField(label='Salary',
                             widget=forms.TextInput(attrs={'placeholder': 'i.e Negotiable'}),
                             required=False)
    benefits = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'i.e Accommodation provided'}),
                               empty_value='',
                               required=False)

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'contact_name', 'contact_email',
                  'contact_number', 'schedule', 'other_requirements', 'is_full_time',
                  'pay_rate', 'salary', 'benefits']


class TakeDownJobForm(forms.ModelForm):
    """Form for recruiters to hide their job post from the public."""
    is_visible = forms.HiddenInput()

    def save(self, commit=True):
        """
        Hook into the save to update the visibility field.

        :param commit:
        :return:
        """

        self.instance.is_visible = False

        return super(TakeDownJobForm, self).save(commit=commit)

    class Meta:
        model = JobPost
        fields = ['is_visible']


class ApplyToJobForm(forms.Form):
    email_body = forms.CharField(widget=forms.Textarea)
    resume = forms.FileField()
    contact_email = forms.EmailField(label='Your email [You will receive a copy of this email]', max_length=255)
