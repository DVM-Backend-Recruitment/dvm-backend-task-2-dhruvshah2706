"""
URL configuration for movie project.

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
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', users_views.custom_login, name='login'),
    path('logout/', users_views.custom_logout, name='logout'),
    path('register/', users_views.register, name='register'),
    path('dashboard/', users_views.dashboard_redirect, name='dashboard_redirect'),
    path('', include('ticket.urls')),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('accounts/', include('allauth.urls')),
]
