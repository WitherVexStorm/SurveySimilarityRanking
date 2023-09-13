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
from . import views

urlpatterns = [
    path('', views.list_surveys, name='list-surveys'),
    path('create/', views.create_survey, name='create-survey'),
    path('fill/', views.fill_survey, name='fill-survey'),
    path('find-similarity/', views.find_similarity, name='find-similarity'),
    path('find-similarity-to/', views.find_similarity_to, name='find-similarity-to'),
    path('find-similarity-between/', views.find_similarity_between, name='find-similarity-between'),
    path('find-similarity-paged/', views.find_similarity_paged, name='find-similarity-paged'),
]
