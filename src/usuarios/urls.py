from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('mudar_senha/', views.mudar_senha, name='mudar_senha'),
    path('valida_cadastro/', views.valida_cadastro, name='valida_cadastro'),
    path('valida_login/', views.valida_login, name='valida_login'),
    path('valida_mudanca_senha/', views.valida_mudanca_senha, name='valida_mudanca_senha'),
    path('sair/', views.sair, name='sair'),
    path('mudarDados/', views.mudarDados, name='mudarDados'),
    path('alterarDados/', views.alterarDados, name='alterarDados'),
    path('perfil/', views.perfil, name='perfil')
]
