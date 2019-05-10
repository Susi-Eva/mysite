from django.urls import path
from apps import views
from . import views

app_name = 'apps'



urlpatterns = [
    path('', views.home),
    path('index/', views.index),
    path('search/', views.search),
]