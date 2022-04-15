from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Filme, Banner, Elenco, Nomination

import random

MELHORES_BANNERS = [
    'https://www.themoviedb.org//t/p/original/qXMXmhsJeW28DYp5iOar9BGepVS.jpg',
    'https://image.tmdb.org//t/p/original/rg5cwyR9UflxJigmBSG47h7MI5w.jpg',
    'https://image.tmdb.org//t/p/original/5RuR7GhOI5fElADXZb0X2sr9w5n.jpg',
    'https://image.tmdb.org//t/p/original/45NaUHojRMGVn54AjoyxVWsMx03.jpg',
    'https://image.tmdb.org//t/p/original/xMJvffWIaW9MtlY9aIXKViUNeIO.jpg',
    'https://image.tmdb.org//t/p/original/sMYhsydRtuOmYZYLrQZWaNZ6nIY.jpg',
    'https://image.tmdb.org//t/p/original/sfjqJDmNqMIImO5khiddb9TARvO.jpg',
    'https://image.tmdb.org//t/p/original/lzWHmYdfeFiMIY4JaMmtR7GEli3.jpg',
    'https://image.tmdb.org//t/p/original/cS9wPYC99khLSBKvmhLATAVa19x.jpg',
    'https://image.tmdb.org//t/p/original/v85FlkbMYKa5du1glm0YfYNsL2n.jpg']

CATEGORIAS = [
    ["Best Picture ", "Melhor Filme", "POSTER"], 
    ["Director ", "Melhor Diretor(a)"], 
    ["Actor ", "Melhor Ator"], 
    ["Actress ", "Melhor Atriz"], 
    ["Supporting Actor ", "Melhor Ator Coadjuvante"], 
    ["Supporting Actor ", "Melhor Atriz Coadjuvante"],
    ["Adapted Screenplay ", "Melhor Roteiro Adaptado"],
    ["Original Screenplay ", "Melhor Roteiro Original"],
    ["Cinematography ", "Melhor Fotografia"],
    ["Original Score ", "Melhor Trilha Sonora"],
    ["Original Song ", "Melhor Canção Original"],
    ["Film Editing ", "Melhor Edição"],
    ["Costume Design ", "Melhor Figurino"],
    ["Makeup and Hairstyling ", "Melhor Maquiagem"],
    ["Production Design ", "Melhor Design de Produção"],
    ["International Feature ", "Melhor Filme Internacional"],
    ["Documentary Feature ", "Melhor Documentário"],
    ["Documentary Short ", "Melhor Cura Documentário"],
    ["Animated Feature ", "Melhor Animação"],
    ["Animated Short ", "Melhor Curta Animado"],
    ["Live Action Short ", "Melhor Curta Metragem"],
    ["Sound ", "Melhor Som"],
    ["Visual Effects ", "Melhores Efeitos Visuais"]
    ]

# Create your views here.
def filmes(request):
    status = request.GET.get('status')
    nome = list(Filme.objects.all())
    return render(request, 'filmes.html', {
        "status": status, 
        "nome":nome,
        "banner": random.choice(MELHORES_BANNERS) 
        #"banner":pegaBanner(random.randint(0, 53))
        })

def pegaFilme(id_filme):
    todos = list(Filme.objects.all().filter(id=id_filme))

    if len(todos) > 0:
        return todos[0]
    else:
        return []

def pegaBanner(id_filme):
    todos = list(Banner.objects.all().filter(id_filme=id_filme))

    if len(todos) > 0:
        return todos[random.randint(0, len(todos)-1)].banner;
    else:
        return 'https://png.pngtree.com/thumb_back/fh260/background/20200821/pngtree-solid-black-solid-color-background-image_396551.jpg'

def pegaElenco(id_filme):
    todos = list(Elenco.objects.all().filter(id_filme=id_filme))

    if len(todos) > 0:
        return todos;
    else:
        return []

def pegaNomeacoes(id_filme):
    todos = list(Nomination.objects.all().filter(id_filme=id_filme))
    if len(todos) > 0:
        return todos;
    else:
        return []

def bestPicture(nomeacoes):
    for i in nomeacoes:
        if i.categoria == 'Best Picture ':
            return 'T'
    return 'F'

def pegaEstadoTomatoe(tomatoes):

    if tomatoes >= 70:
        retorno = 'https://www.rottentomatoes.com/assets/pizza-pie/images/icons/tomatometer/certified_fresh.75211285dbb.svg'
    elif tomatoes < 70 and tomatoes >= 60:
        retorno = 'https://www.rottentomatoes.com/assets/pizza-pie/images/icons/tomatometer/tomatometer-fresh.149b5e8adc3.svg'
    elif tomatoes == -1:
        retorno = 'https://www.rottentomatoes.com/assets/pizza-pie/images/icons/tomatometer/tomatometer-empty.cd930dab34a.svg'
    else:
        retorno = 'https://www.rottentomatoes.com/assets/pizza-pie/images/icons/tomatometer/tomatometer-rotten.f1ef4f02ce3.svg'

    return retorno

def filme(request, nome):
    status = request.GET.get('status')
    aux = Filme.objects.filter(nome=nome)[0]
    banner = pegaBanner(aux.id)
    elenco = pegaElenco(aux.id)
    genero = str(aux.genero).split(';')[0]
    nomeacoes = pegaNomeacoes(aux.id)
    bestPic = bestPicture(nomeacoes)
    return render(request, 'filme_solo.html', {
        "status":status, 
        "filme":aux, 
        "banner":banner,
        "elenco":elenco,
        "genero":genero,
        "nomeacoes":nomeacoes,
        "qntNomeacoes":len(nomeacoes),
        "posicao":(int(aux.id)+1),
        "bestPic":bestPic,
        "estadoTomatoe":pegaEstadoTomatoe(aux.tomatoes)
    })

def buscaCategoriaPortugues(categoria):

    i = 0
    retorno = -1

    while(retorno == -1 and i < len(CATEGORIAS)):
        if categoria == CATEGORIAS[i][0]:
            retorno = i
        i += 1
    
    return retorno

def pegaCategoria(categoria):
    todos = list(Nomination.objects.all().filter(categoria=categoria))
    retorno = []
    for i in todos:
        retorno.append(
            pegaFilme(id_filme=i.id_filme)
        )
    return {
        "Categoria": CATEGORIAS[buscaCategoriaPortugues(categoria)][1],
        "Indicados": retorno
    }