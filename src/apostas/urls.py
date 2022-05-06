from django.urls import path
from . import views

urlpatterns = [
    path('categorias/', views.categorias, name='categorias'),
    path('montar/?P<categoria>[-a-zA-Z0-9_]+)\\Z/', views.montar, name='montar'),
    path('resultados/', views.resultados, name='resultados'),
    path('verificar/?P<categoria>[-a-zA-Z0-9_]+)\\Z/', views.verificar, name='verificar'),
    path('finalizar/', views.finalizar, name='finalizar'),
    path('salvaAposta/', views.salvaAposta, name='salvaAposta'),
    path('apostaFeita/<int:id_aposta>/', views.apostaFeita, name='apostaFeita'),
]