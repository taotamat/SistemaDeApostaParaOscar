from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from filmes.views import pegaBanner, pegaCategoria, pegaCategoriasPT, CATEGORIAS, MELHORES_BANNERS
import random

# Create your views here.
def categorias(request):
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    return render(request, 'categorias.html', {
        'status': status, 
        'id_user':id_usuario,
        "banner": random.choice(MELHORES_BANNERS),
        'categoriasTodas': pegaCategoriasPT()
        }
    )
