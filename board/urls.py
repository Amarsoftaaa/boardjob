from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import *

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path("login/", LoginView.as_view(template_name="board/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('jobs/',JobListView.as_view(),name='job_list'),
    path('jobs/<slug:slug>/<int:pk>/',JobDetailView.as_view(),name='job_detail'),
    path('job_create/',JobCreateView.as_view(),name='job_create'),
    path('register_company/',RegisterCompanyView.as_view(),name='register_company'),
    path('company',TemplateView.as_view(template_name="board/company.html"), name="company"),
    path('register_candidate/',RegisterCandidateView.as_view(),name='register_candidate'),
    path('profil',ProfilPageView.as_view(template_name="board/profil.html"), name="profil"),
    path('job_aplication',TemplateView.as_view(template_name="board/job_aplication.html"), name="job_aplication"),



]