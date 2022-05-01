from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from filmes.views import pegaBanner, pegaCategoria, pegaCategoriasPT, CATEGORIAS, MELHORES_BANNERS
from apostas.forms import *
import random

# Create your views here.
def categorias(request):
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    return render(request, 'categorias.html', {
        'status': status, 
        'id_user':id_usuario,
        "banner": random.choice(MELHORES_BANNERS),
        'categoriasTodas': CATEGORIAS
        }
    )


def montar(request, categoria):
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    c = pegaCategoria(categoria)
    
    if len(c['Indicados'])>5:
        tam = 10
        formulario = Aposta10()
#        if request.method == 'POST':
#            formulario = Aposta10(request.POST)
#            if formulario.is_valid():
#                formulario.save()
    else:
        tam = 5
        formulario = Aposta5()
#        if request.method == 'POST':
#            formulario = Aposta5(request.POST)
#            if formulario.is_valid():
#                formulario.save()

    return render(request, 'aposta.html', {
        'form':formulario,
        'status': status, 
        'id_user':id_usuario,
        'categoria': c['Categoria'],
        "banner": random.choice(MELHORES_BANNERS),
        'indicados': c['Indicados'],
        'qnt': tam
        
        }
    )

#def finalizar(request, aposta):
