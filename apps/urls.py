from django.urls import path
from apps import views
from . import views

app_name = 'apps'



urlpatterns = [
    path('', views.home),
    path('index/', views.index),
    path('index2/', views.index2),
    path('index3/', views.index3),
    path('result/', views.result),
    path('result2/', views.result2),
    path('result3/', views.result3),
    path('lyric/<int:id>', views.lyric, name='lyric'),
    path('lyric2/<int:nomor>', views.lyric2, name='lyric2'),
    path('lyric3/<int:nomor>', views.lyric3, name='lyric3'),
]