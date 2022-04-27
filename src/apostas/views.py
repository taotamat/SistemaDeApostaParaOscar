from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from filmes.views import pegaBanner, pegaCategoria, pegaCategoriasPT, CATEGORIAS, MELHORES_BANNERS
from .models import Resultado
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
    return render(request, 'aposta.html', {
        'status': status, 
        'id_user':id_usuario,
        'categoria': c['Categoria'],
        'indicados': c['Indicados']
        }
    )

def resultados(request):
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    resultadosL = list(Resultado.objects.all())
    return render(request, 'resultados.html', {
        'status': status, 
        'id_user':id_usuario,
        'categoriasTodas': CATEGORIAS,
        "banner": random.choice(MELHORES_BANNERS),
        'temResultados':len(resultadosL),
        'resultadosL': resultadosL
        }
    )