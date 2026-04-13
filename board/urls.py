from django.urls import path
from board import views

from django.contrib.auth.views import LoginView,LogoutView
from .views import *

urlpatterns = [
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path('',HomePageView.as_view(),name='home'),
    path("login/", LoginView.as_view(template_name="board/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('jobs/',JobListView.as_view(),name='job_list'),
    path('jobs/<slug:slug>/<int:pk>/',JobDetailView.as_view(),name='job_detail'),
    path('job_create/',JobCreateView.as_view(),name='job_create'),
    path('register_company/',RegisterCompanyView.as_view(),name='register_company'),
    path('company', TemplateView.as_view(template_name="board/company_profile.html"), name="company"),
    path('register_candidate/',RegisterCandidateView.as_view(),name='register_candidate'),
    path('profil/',ProfilPageView.as_view(), name="profil"),
    path("jobs/<int:pk>/apply/", JobApplicationView.as_view(), name="apply_job"),
    path("inbox/",InboxView.as_view(), name="inbox"),
    path("message/send/<int:user_id>/", views.SendMessageView.as_view(), name="send_message"),

    path("candidate/<int:user_id>/", views.CandidatePublicProfileView.as_view(), name="candidate_profile"),

    path("apply/<int:job_id>/", views.apply_for_job, name="apply_for_job"),
    path("company/applications/", views.company_applications, name="company_applications"),
    path(
    "company/applications/<int:application_id>/<str:new_status>/",
    views.update_application_status,
    name="update_application_status"
),

]