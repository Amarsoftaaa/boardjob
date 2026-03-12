from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CompanyRegisterForm(UserCreationForm):
    company_name = forms.CharField(max_length=100)
    website = forms.URLField(required=False)
    location = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "password1", "password2", "company_name", "website", "location")



class CandidateRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "password1", "password2", "first_name", "last_name","email", "location", "birth_date")

INPUT_CLASS = (
    "w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-2 "
    "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
)

class CandidateCVForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['cv']





class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','location','job_type','employment_type','is_active']
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-3 h-40 resize-none focus:ring-2 focus:ring-indigo-500 focus:outline-none",
                "placeholder": "Describe the job in detail..."
            }),
            "location": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            }),
            "job_type": forms.Select(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            }),
            "employment_type": forms.Select(attrs={
                "class": "w-full rounded-lg border border-slate-300 px-4 py-2 bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
            }),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "w-full min-h-[180px] rounded-xl border border-gray-300 px-4 py-3 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",

                "rows": 5,
                "placeholder": "Write a message..."
            })
        }
        labels = {
            "content": ""
        }

    def clean_content(self):
        content = self.cleaned_data["content"].strip()
        if not content:
            raise forms.ValidationError("Message cannot be empty..")
        return content


