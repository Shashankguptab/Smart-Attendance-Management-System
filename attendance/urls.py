from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/",auth_views.LoginView.as_view(template_name="attendance/login.html"),name="login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("attendance/mark/",views.mark_attendance,name="mark_attendance"),
    path("attendance/history/",views.attendance_history,name="attendance_history"),
    path("attendance/session/<int:session_id>/",views.session_detail,name="session_detail"),
    path("attendance/edit/<int:record_id>/",views.edit_attendance,name="edit_attendance"),
    path("attendance/low/",views.low_attendance,name="low_attendance"),

    
]