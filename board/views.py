from http.client import HTTPResponse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render

from board.forms import JobForm
from board.models import Job


class HomePageView(TemplateView):
    template_name = 'board/index.html'

class ProfilPageView(TemplateView):
    template_name = 'board/profil.html'

def job_detail(request):
    return render(request,'board/job_detail.html')

class JobListView(ListView):
    model = Job
    template_name = 'board/job_list.html'

class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'board/job_form.html'
