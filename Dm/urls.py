"""Dm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
from Ms.views import mensajes_privados_view, DetailMs, ChanelDetail, inicio



UUID_CHANNEL_REGEX = r'channel/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(UUID_CHANNEL_REGEX, ChanelDetail.as_view(), name="mss"),
    path("dm/<str:username>", mensajes_privados_view),
    path("ms/<str:username>", DetailMs.as_view(), name="usern"),

    path('', inicio.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),

]
