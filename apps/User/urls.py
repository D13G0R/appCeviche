from django.urls import path
from apps.User import views

urlpatterns = [
    path("register/", views.register, name = "registerUser"),
]