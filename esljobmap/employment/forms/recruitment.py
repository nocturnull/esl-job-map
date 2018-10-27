# employment/forms/recruitment.py
from django import forms
from ..models.recruitment import JobPost


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


class CreateFullTimeJobForm(CreateJobForm):
    salary = forms.CharField(label='Salary',
                             widget=forms.TextInput(attrs={'placeholder': 'Ex) Negotiable'}),
                             required=True)
    benefits = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ex) Accommodation provided'}),
                               empty_value='')

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'contact_name', 'contact_email',
                  'contact_number', 'schedule', 'other_requirements', 'is_full_time',
                  'salary', 'benefits', 'latitude', 'longitude', 'address']


class CreatePartTimeJobForm(CreateJobForm):
    pay_rate = forms.CharField(label='Pay Rate',
                               widget=forms.TextInput(attrs={'placeholder': 'Ex) 45,000 per hour'}))

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'contact_name', 'contact_email',
                  'contact_number', 'schedule', 'other_requirements', 'is_full_time',
                  'pay_rate', 'latitude', 'longitude', 'address']


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
    resume = forms.FileField(allow_empty_file=True, required=False)
    contact_email = forms.EmailField(label='Your email [You will receive a copy of this email]', max_length=255)
    use_existing_resume = forms.BooleanField(required=False)
