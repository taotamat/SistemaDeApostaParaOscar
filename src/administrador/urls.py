from django.urls import path
from . import views

urlpatterns = [
    path('', views.administrador, name='administrador'),
    path('login/', views.administrador, name='loginA'),
    path('valida_loginA/', views.valida_loginA, name='valida_loginA'),
    path('home/', views.home, name='homeA'),
    path('cadResultados/', views.cadResultados, name='cadResultados'),
    path('valida_resultados/', views.valida_resultados, name='valida_resultados'),
    path('salvar_resultados/', views.salvar_resultados, name='salvar_resultados'),
    path('sairA/', views.sairA, name='sairA')
]