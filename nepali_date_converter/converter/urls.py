from django.contrib import admin
from django.urls import path
from converter import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('convert/', views.convert_date, name='convert_date'),
]
