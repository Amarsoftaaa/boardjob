from http.client import HTTPResponse
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.shortcuts import render,redirect

from .forms import *
from .models import *


class HomePageView(TemplateView):
    template_name = 'board/index.html'


class ProfilPageView(UpdateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = "board/profil.html"
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        obj, created = CandidateProfile.objects.get_or_create(
            user=self.request.user
        )
        return obj

class JobDetailView(DetailView):
    model = Job
    template_name = 'board/job_detail.html'
    context_object_name = 'job'

class JobListView(ListView):
    model = Job
    template_name = 'board/job_list.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        qs = Job.objects.filter(is_active=True)

        # postojeći filteri
        job_type = self.request.GET.get("job_type")
        employment_type = self.request.GET.get("employment_type")

        if job_type:
            qs = qs.filter(job_type=job_type)
        if employment_type:
            qs = qs.filter(employment_type=employment_type)

        # SEARCH
        q = self.request.GET.get("q")
        location = self.request.GET.get("location")

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(company__company_name__icontains=q)  # ako ti je company.name
            )

        if location:
            qs = qs.filter(location__icontains=location)

        return qs


class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'board/job_form.html'
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "company_profile"):
            return redirect("company_profile_create")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        job = form.save(commit=False)
        job.company = self.request.user.company_profile
        job.save()
        return super().form_valid(form)


class RegisterCompanyView(CreateView):
    form_class = CompanyRegisterForm
    template_name = "board/register_company.html"
    success_url = reverse_lazy("login")

    @transaction.atomic
    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = CustomUser.Role.COMPANY
        user.save()

        Company.objects.create(
            user=user,
            company_name=form.cleaned_data["company_name"],
            website=form.cleaned_data.get("website", ""),
            location=form.cleaned_data["location"],
        )

        self.object = user

        return redirect(self.get_success_url())


class RegisterCandidateView(CreateView):
    form_class = CandidateRegisterForm
    template_name = "board/register_candidate.html"
    success_url = reverse_lazy("login")

    @transaction.atomic
    def form_valid(self, form):
        user = form.save(commit=False)
        user.role = CustomUser.Role.CANDIDATE
        user.save()

        CandidateProfile.objects.create(
            user=user,
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            location=form.cleaned_data["location"],
            birth_date=form.cleaned_data.get("birth_date"),
        )

        self.object = user

        return redirect(self.get_success_url())

class JobAplicationView(CreateView):
    template_name = "board/job_aplication.html"
    model = Application
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "candidate_profile"):
            return redirect("candidate_profile_create")
        return super().dispatch(request, *args, **kwargs)

    def user_valid(self):
        job = form.save(commit=False)
        job.company = self.request.user.candidate_profile
        job.save()
        return super().form_valid(form)


