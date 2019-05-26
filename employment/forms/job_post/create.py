# employment/forms/job_post/create.py

from django import forms

from employment.models.recruitment import JobPost


class CreateJobForm(forms.ModelForm):
    """Form for recruiters to create a new job post."""
    JOB_TYPE_CHOICES = ((True, 'Full-time'), (False, 'Part-time'))

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Give a short, descriptive title!'}))
    class_type = forms.CharField(label='Class Type', widget=forms.TextInput(attrs={'placeholder': 'Ex) 1:1 Business English / Speaking'}))
    schedule = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ex) Mon-Fri 9-6'}))
    other_requirements = forms.CharField(label='Other Requirements', widget=forms.TextInput(attrs={'placeholder': 'Ex) Teaching certificate'}), required=False)


class CreateFullTimeJobForm(CreateJobForm):
    salary = forms.CharField(label='Salary',
                             widget=forms.TextInput(attrs={'placeholder': 'Ex) Negotiable'}))
    benefits = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ex) Accommodation provided'}),
                               required=False,
                               empty_value='')

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'schedule', 'other_requirements',
                  'is_full_time', 'salary', 'benefits', 'latitude', 'longitude', 'address']


class CreatePartTimeJobForm(CreateJobForm):
    pay_rate = forms.CharField(label='Pay Rate',
                               widget=forms.TextInput(attrs={'placeholder': 'Ex) 45,000 per hour'}),
                               required=True)

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'schedule', 'other_requirements',
                  'is_full_time', 'pay_rate', 'latitude', 'longitude', 'address']
