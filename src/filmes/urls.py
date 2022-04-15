from django.urls import path
from . import views

urlpatterns = [
    path('', views.filmes, name='filmes'),
    path('home/', views.filmes, name='filmes'),
    path('filme/?P<nome>[-a-zA-Z0-9_]+)\\Z', views.filme, name='filme')
]