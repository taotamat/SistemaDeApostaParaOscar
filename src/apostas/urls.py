from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.categorias, name='categorias'),
    path('montar/?P<categoria>[-a-zA-Z0-9_]+)\\Z', views.montar, name='montar'),
    path('resultados/', views.resultados, name='resultados')
]