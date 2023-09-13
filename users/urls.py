"""
URL configuration for django_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from django.contrib.auth import views as ready_views
from . import views

urlpatterns = [
    path('login/', ready_views.LoginView.as_view(template_name='users/login.html'), name='login-user'),
    path('logout/', ready_views.LogoutView.as_view(template_name='users/logout.html'), name='logout-user'),
    path('register/', views.register, name='register-user'),
]
