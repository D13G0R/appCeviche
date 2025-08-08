from django.urls import path
from apps.User import views

urlpatterns = [
    path("register/", views.registerUser, name = "registerUser"),
    path("login/", views.loginUser, name = "loginUser")
]