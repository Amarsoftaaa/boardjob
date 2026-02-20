from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from board import views
from board.views import HomePageView,JobListView,JobCreateView,TemplateView

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('jobs/',JobListView.as_view(),name='job_list'),
    path('job_detail',views.job_detail,name='job_detail'),
    path('jobcreate/',JobCreateView.as_view(),name='job_create'),
    path("login/", LoginView.as_view(template_name="board/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('profil',TemplateView.as_view(template_name="board/profil.html"), name="profil"),
    path('company',TemplateView.as_view(template_name="board/company.html"), name="company"),

]