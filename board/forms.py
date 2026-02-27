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
        fields = ("username", "password1", "password2", "first_name", "last_name", "location", "birth_date")

INPUT_CLASS = (
    "w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-2 "
    "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
)





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
                "placeholder": "Detaljno opišite posao..."
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


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        # prikazi sva polja osim user (user se ne uređuje)
        fields = ["email", "first_name", "last_name", "location", "birth_date", "cv"]

        widgets = {
            "email": forms.EmailInput(attrs={"class": "w-full border rounded p-2"}),
            "first_name": forms.TextInput(attrs={"class": "w-full border rounded p-2"}),
            "last_name": forms.TextInput(attrs={"class": "w-full border rounded p-2"}),
            "location": forms.TextInput(attrs={"class": "w-full border rounded p-2"}),
            "birth_date": forms.DateInput(attrs={"type": "date", "class": "w-full border rounded p-2"}),
            "cv": forms.ClearableFileInput(attrs={"class": "w-full border rounded p-2"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ polja koja NE želiš da korisnik uređuje (ali želiš da ih vidi)
        readonly_fields = ["email"]  # npr. email ne može mijenjati

        for f in readonly_fields:
            if f in self.fields:
                self.fields[f].disabled = True  # read-only u formi

