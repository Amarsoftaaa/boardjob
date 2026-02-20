from django import forms
from .models import *

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','location','job_type','is_active']
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

            "is_active": forms.CheckboxInput(attrs={
                "class": "h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
            }),
        }

