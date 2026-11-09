"""URL configuration for the online course project."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from onlinecourse_app import views

urlpatterns = [
    path("", views.course_list, name="home"),
    path("admin/", admin.site.urls),
    path("onlinecourse/", include("onlinecourse_app.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="onlinecourse_app/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
]
