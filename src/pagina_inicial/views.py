from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from hashlib import sha256
from usuarios.models import Usuario
from filmes.views import pegaBanner, pegaCategoria, CATEGORIAS, MELHORES_BANNERS
import random
# 

def home(request):

    id_user = request.session.get('usuario')

    if id_user == None:
        retorno = redirect('/auth/login/?status=3')
    else:
        usuario = Usuario.objects.filter(id=id_user)[0]

        indicados = pegaCategoria(categoria=CATEGORIAS[0][0])

        retorno = render(request, 'home.html', {
            "nome": usuario.nome,
            "banner": random.choice(MELHORES_BANNERS),
            "indicados": indicados,
            "id_user": id_user
            }
        )
    
    return retorno


def creditos(request):
    id_user = request.session.get('usuario')
    status = request.GET.get('status')
    return render(request, 'creditos.html', {
        'status': status,
        'id_user': id_user,
        "banner": random.choice(MELHORES_BANNERS)
        }
    )
