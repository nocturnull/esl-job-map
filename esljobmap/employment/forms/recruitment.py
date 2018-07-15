# employment/forms/recruitment.py
from django import forms
from ..models.recruitment import JobPost


class JobCreationForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'i.e Seeking Full Time Teacher in Gangnam'}))
    class_type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'i.e First Grade/High School'}))
    schedule = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'i.e 9AM-1PM M-F '}))

    class Meta:
        model = JobPost
        fields = ['title', 'class_type', 'contact_name', 'contact_email',
                  'contact_number', 'schedule', 'other_requirements', 'is_full_time',
                  'pay_rate', 'salary', 'benefits']
