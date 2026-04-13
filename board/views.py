from http.client import HTTPResponse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


class HomePageView(TemplateView):
    template_name = 'board/index.html'



class ProfilPageView(LoginRequiredMixin, TemplateView):
    template_name = "board/candidate_profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == CustomUser.Role.COMPANY:
            return redirect("company")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(CandidateProfile, user=self.request.user)
        applications = Application.objects.filter(
            candidate=profile
        ).select_related("job", "job__company").order_by("-created_at")

        context["profile"] = profile
        context["applications"] = applications
        return context

    def post(self, request, *args, **kwargs):
        if request.user.role == CustomUser.Role.COMPANY:
            return redirect("company")

        profile = get_object_or_404(CandidateProfile, user=request.user)

        if request.FILES.get("cv"):
            profile.cv = request.FILES["cv"]
            profile.save()

        return redirect("profil")


class CompanyPageView(LoginRequiredMixin, TemplateView):
    template_name = "board/company_profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.role == CustomUser.Role.CANDIDATE:
            return redirect("profil")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company = get_object_or_404(Company, user=self.request.user)

        jobs = Job.objects.filter(company=company).order_by("-created_at")

        applications = Application.objects.filter(
            job__company=company
        ).select_related("candidate", "candidate__user", "job").order_by("-created_at")

        conversations_count = Conversation.objects.filter(
            participants=self.request.user
        ).distinct().count()

        context["company"] = company
        context["jobs"] = jobs
        context["applications"] = applications
        context["conversations_count"] = conversations_count
        return context



class CandidatePublicProfileView(LoginRequiredMixin, TemplateView):
    template_name = "board/candidate_public_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.kwargs["user_id"]
        profile = get_object_or_404(CandidateProfile, user_id=user_id)

        context["profile"] = profile
        return context



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
        messages.success(self.request, "The ad was successfully published.")
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

        messages.success(self.request, "You have successfully registered company.")
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

        messages.success(self.request, "You have successfully registered.")
        return redirect(self.get_success_url())

class JobApplicationView(LoginRequiredMixin, CreateView):
    template_name = "board/job_aplication.html"
    model = Application
    fields = []  # ako nemaš dodatna polja (npr cover_letter). Ako imaš, stavi ih ovdje.
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "candidate_profile"):
            return redirect("candidate_profile_create")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        job = get_object_or_404(Job, pk=self.kwargs["pk"])
        candidate = self.request.user.candidate_profile

        # 🔥 PROVJERA DA LI VEĆ POSTOJI PRIJAVA
        if Application.objects.filter(job=job, candidate=candidate).exists():
            messages.warning(self.request, "You have already applied for this job.")
            return redirect("job_detail", pk=job.pk, slug=job.slug)  # prilagodi ako treba

        # ako ne postoji → snimi
        form.instance.job = job
        form.instance.candidate = candidate

        messages.success(self.request, "You have successfully applied.")
        return super().form_valid(form)

User = get_user_model()

class SendMessageView(LoginRequiredMixin, CreateView):
    model = Messages
    form_class = MessageForm
    template_name = "board/send_message.html"

    def dispatch(self, request, *args, **kwargs):
        self.receiver = get_object_or_404(User, id=self.kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = self.receiver
        return super().form_valid(form)

    def get_success_url(self):
        return f"{reverse_lazy('inbox')}?user={self.receiver.id}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["receiver"] = self.receiver
        return context

class InboxView(LoginRequiredMixin, TemplateView):
    template_name = "board/inbox.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        selected_user_id = self.request.GET.get("user")

        all_messages = Messages.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by("-created_at")

        conversations = []
        seen_users = set()

        for message in all_messages:
            other_user = message.receiver if message.sender == user else message.sender

            if other_user.id not in seen_users:
                unread_count = Messages.objects.filter(
                    sender=other_user,
                    receiver=user,
                    is_read=False
                ).count()

                if hasattr(other_user, "companyprofile") and other_user.companyprofile.company_name:
                    display_name = other_user.companyprofile.company_name
                elif other_user.first_name or other_user.last_name:
                    display_name = f"{other_user.first_name} {other_user.last_name}".strip()
                else:
                    display_name = other_user.username

                conversations.append({
                    "user": other_user,
                    "last_message": message,
                    "unread_count": unread_count,
                    "display_name": display_name,
                })
                seen_users.add(other_user.id)

        selected_user = None
        chat_messages = None
        selected_display_name = None

        if selected_user_id:
            try:
                selected_user = User.objects.get(id=selected_user_id)
                if hasattr(selected_user, "companyprofile") and selected_user.companyprofile.company_name:
                    selected_display_name = selected_user.companyprofile.company_name
                elif selected_user.first_name or selected_user.last_name:
                    selected_display_name = f"{selected_user.first_name} {selected_user.last_name}".strip()
                else:
                    selected_display_name = selected_user.username

                chat_messages = Messages.objects.filter(
                    Q(sender=user, receiver=selected_user) |
                    Q(sender=selected_user, receiver=user)
                ).order_by("created_at")

                Messages.objects.filter(
                    sender=selected_user,
                    receiver=user,
                    is_read=False
                ).update(is_read=True)

            except User.DoesNotExist:
                selected_user = None
                chat_messages = None
                selected_display_name = None

        context["conversations"] = conversations
        context["selected_user"] = selected_user
        context["chat_messages"] = chat_messages
        context["selected_display_name"] = selected_display_name
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        selected_user_id = request.GET.get("user")
        content = request.POST.get("content")

        if selected_user_id and content:
            try:
                receiver = User.objects.get(id=selected_user_id)

                Messages.objects.create(
                    sender=user,
                    receiver=receiver,
                    content=content
                )
            except User.DoesNotExist:
                pass

        return redirect(f"{request.path}?user={selected_user_id}")


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /inbox/",
        "Disallow: /profil/",
        "Disallow: /company/applications/",
        "Disallow: /message/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role != "CANDIDATE":
        messages.error(request, "Only candidates can apply for jobs.")
        return redirect("job_detail", slug=job.slug)

    candidate = request.user.candidate_profile

    already_applied = Application.objects.filter(candidate=candidate, job=job).exists()
    if already_applied:
        messages.warning(request, "You have already applied for this job.")
        return redirect("job_detail", slug=job.slug)

    Application.objects.create(
        candidate=candidate,
        job=job,
        status="submitted"
    )

    messages.success(request, "Application submitted successfully.")
    return redirect("candidate_profile")

@login_required
def company_applications(request):
    if request.user.role != "COMPANY":
        return redirect("home")

    company = request.user.company_profile

    applications = Application.objects.filter(
        job__company=company
    ).select_related(
        "candidate__user",
        "job",
        "job__company"
    ).order_by("-created_at")

    return render(request, "board/company_applications.html", {
        "applications": applications
    })

@login_required
def update_application_status(request, application_id, new_status):
    if request.user.role != "COMPANY":
        return redirect("home")

    application = get_object_or_404(Application, id=application_id)

    if application.job.company != request.user.company_profile:
        return HttpResponseForbidden("You are not allowed to update this application.")

    allowed_statuses = ["submitted", "viewed", "rejected"]

    if new_status in allowed_statuses:
        application.status = new_status
        application.save()

    return redirect("company_applications")

