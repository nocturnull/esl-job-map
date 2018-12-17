# employment/forms/recruitment.py

from django import forms
from ..models.recruitment import JobPost
from account.templatetags.profile import is_recruiter


class CreateJobForm(forms.ModelForm):
    """Form for recruiters to create a new job post."""
    JOB_TYPE_CHOICES = ((True, 'Full-time'), (False, 'Part-time'))

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Give a short, descriptive title!'}))
    class_type = forms.CharField(label='Class Type', widget=forms.TextInput(attrs={'placeholder': 'Ex) 1:1 Business English / Speaking'}))
    contact_name = forms.CharField(label='Contact Name', widget=forms.TextInput(attrs={'placeholder': 'Ex) Your name'}))
    contact_email = forms.CharField(label='Contact Email', widget=forms.TextInput(attrs={'placeholder': 'Ex) name@email.com'}))
    contact_number = forms.CharField(label='Contact Number', widget=forms.TextInput(attrs={'placeholder': 'Ex) 010-0000-0000'}), required=False)
    schedule = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ex) Mon-Fri 9-6'}))
    other_requirements = forms.CharField(label='Other Requirements', widget=forms.TextInput(attrs={'placeholder': 'Ex) Teaching certificate'}), required=False)

    def __init__(self, request=None, *args, **kwargs):
        """Constructor override"""
        super(CreateJobForm, self).__init__(*args, **kwargs)
        if is_recruiter(request):
            user = request.user
            self.fields['contact_name'].initial = user.full_name
            self.fields['contact_email'].initial = user.email
            self.fields['contact_number'].initial = user.phone_number


class CreateFullTimeJobForm(CreateJobForm):
    salary = forms.CharField(label='Salary',
                             widget=forms.TextInput(attrs={'placeholder': 'Ex) Negotiable'}))
    benefits = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ex) Accommodation provided'}),
                               required=False,
                               empty_value='')

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'contact_name', 'contact_email',
                  'contact_number', 'schedule', 'other_requirements', 'is_full_time',
                  'salary', 'benefits', 'latitude', 'longitude', 'address']


class CreatePartTimeJobForm(CreateJobForm):
    pay_rate = forms.CharField(label='Pay Rate',
                               widget=forms.TextInput(attrs={'placeholder': 'Ex) 45,000 per hour'}),
                               required=True)

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'contact_name', 'contact_email',
                  'contact_number', 'schedule', 'other_requirements', 'is_full_time',
                  'pay_rate', 'latitude', 'longitude', 'address']


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


class RepostJobForm(forms.ModelForm):
    """Form for recruiters to repost their job post for the public to see."""
    is_visible = forms.HiddenInput()

    def save(self, commit=True):
        """
        Hook into the save to update the visibility field.

        :param commit:
        :return:
        """

        self.instance.is_visible = True

        return super(RepostJobForm, self).save(commit=commit)

    class Meta:
        model = JobPost
        fields = ['is_visible']


class ArchiveJobForm(forms.ModelForm):
    """Form for recruiters to archive their job post."""
    is_archived = forms.HiddenInput()

    def save(self, commit=True):
        """
        Hook into the save to update the archive field.

        :param commit:
        :return:
        """
        self.instance.is_archived = True

        return super(ArchiveJobForm, self).save(commit=commit)

    class Meta:
        model = JobPost
        fields = ['is_archived']


class ApplyToJobForm(forms.Form):
    email_body = forms.CharField(widget=forms.Textarea(attrs={'rows': '18'}))
    resume = forms.FileField(allow_empty_file=True, required=False)
    contact_email = forms.EmailField(label='Your email [You will receive a copy of this email]', max_length=255)
    use_existing_resume = forms.BooleanField(required=False)
