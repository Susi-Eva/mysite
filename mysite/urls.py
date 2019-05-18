"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path
from apps import views

urlpatterns = [
    path('', views.home),
    path('index/', views.index),
    path('index2/', views.index2),
    path('index3/', views.index3),
    path('result/', views.result),
    path('result2/', views.result2),
    path('result3/', views.result3),
    path('admin/', admin.site.urls),
    path('lyric/<int:id>', views.lyric, name='lyric'),
    path('lyric2/<int:id>', views.lyric2, name='lyric2'),
    path('lyric3/<int:id>', views.lyric3, name='lyric3'),
    path('apps/', include('apps.urls')),
]
