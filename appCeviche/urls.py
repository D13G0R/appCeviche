"""
URL configuration for appCeviche project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import inicio

from rest_framework import routers
from apps.Productos import views
import apps

routes = routers.DefaultRouter()
routes.register("topicsAll", views.TopicViewSet, basename="topicsAll")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio, name = "inicio"),
    
    path('', include('apps.Productos.urls')),
    path('api/', include(routes.urls)),
    path('api/receiveOrder', views.receiveOrder, name = "receiveOrder"),
    path('api/changeDescriptionOrder', views.changeDescriptionOrder, name = 'changeDescriptionOrder'),
    path('', include('apps.User.urls'))
]
