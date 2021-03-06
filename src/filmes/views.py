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
    'https://image.tmdb.org//t/p/original/v85FlkbMYKa5du1glm0YfYNsL2n.jpg',
    'https://image.tmdb.org//t/p/original/dcuGg7tXvkHIUugfIlY1TWVxZQA.jpg',
    'https://image.tmdb.org//t/p/original/3DgGjoMjd188LN4v24Kw7iClKbT.jpg',
    'https://image.tmdb.org//t/p/original/tFwuQaHSFlb6mMDre3zruuux5Vk.jpg',
    'https://image.tmdb.org//t/p/original/CKGSEnFTpcxPJM5TzTFUJz53s.jpg',
    'https://image.tmdb.org//t/p/original/mqDnDhG5N6fn1H4MKQqr8E5wfeK.jpg',
    'https://image.tmdb.org//t/p/original/fIlVvcmfjmbnWSjG9yZkRy9FAmE.jpg',
    'https://image.tmdb.org//t/p/original/95SwyPKoWGK35zOnAjikra7OFIQ.jpg',
    'https://image.tmdb.org//t/p/original/p1eneBfZCGbbzicwksOhIaibUwk.jpg',
    'https://image.tmdb.org//t/p/original/kcUuumAlMWqw7SzXE4DEqd3M8Gc.jpg',
    'https://image.tmdb.org//t/p/original/4KLlHifB1kgMtWl3YnY8JinOj65.jpg',
    'https://image.tmdb.org//t/p/original/kheUYWQcQ340LJDWTgu5STvS1Ma.jpg',
    'https://image.tmdb.org//t/p/original/7CkspL1h98JiqGWKHYdvs88FJSE.jpg',
    'https://image.tmdb.org//t/p/original/aA2ndZKxbEnM2C6PEeg1p3WwPwS.jpg',
    'https://image.tmdb.org//t/p/original/vi5gyubNPhDF7f4HeJvvjZBJzJA.jpg',
    'https://image.tmdb.org//t/p/original/x1d11fjOMGcAsi0ehxJ7l7u7HS2.jpg',
    'https://www.themoviedb.org/t/p/original/620hnMVLu6RSZW6a5rwO8gqpt0t.jpg',
    'https://www.themoviedb.org/t/p/original/g1sQr9ygKhQwMUjIRwkWFvza1S2.jpg',
    'https://image.tmdb.org//t/p/original/neE1BUsnWC0bYIiXbhNwxFgronZ.jpg',
    'https://image.tmdb.org//t/p/original/1E408YATvJ49bjgSzB9YVk8GmTt.jpg',
    'https://image.tmdb.org//t/p/original/pfaog3542ObQ2qONa34Oh8gJ5vq.jpg',
    'https://image.tmdb.org//t/p/original/r4VQbiydjDH7ULo1HWjkkrNt3da.jpg',
    'https://www.themoviedb.org/t/p/original/tHnHTp50qDx7br1i9ulh74MUW0A.jpg',
    'https://image.tmdb.org//t/p/original/nt0TypFdgrPflRyt3ft4PsQQcTC.jpg'
    ]

CATEGORIAS = [
    ["Best Picture ", "Melhor Filme"], 
    ["Director ", "Melhor Diretor(a)"], 
    ["Actor ", "Melhor Ator"], 
    ["Actress ", "Melhor Atriz"], 
    ["Supporting Actor ", "Melhor Ator Coadjuvante"], 
    ["Supporting Actress ", "Melhor Atriz Coadjuvante"],
    ["Adapted Screenplay ", "Melhor Roteiro Adaptado"],
    ["Original Screenplay ", "Melhor Roteiro Original"],
    ["Cinematography ", "Melhor Fotografia"],
    ["Original Score ", "Melhor Trilha Sonora"],
    ["Original Song ", "Melhor Can????o Original"],
    ["Film Editing ", "Melhor Edi????o"],
    ["Costume Design ", "Melhor Figurino"],
    ["Makeup and Hairstyling ", "Melhor Maquiagem"],
    ["Production Design ", "Melhor Design de Produ????o"],
    ["International Feature ", "Melhor Filme Internacional"],
    ["Documentary Feature ", "Melhor Document??rio"],
    ["Documentary Short ", "Melhor Curta Document??rio"],
    ["Animated Feature ", "Melhor Anima????o"],
    ["Animated Short ", "Melhor Curta Animado"],
    ["Live Action Short ", "Melhor Curta Metragem"],
    ["Sound ", "Melhor Som"],
    ["Visual Effects ", "Melhores Efeitos Visuais"]
    ]



# Create your views here.
def filmes(request):
    status = request.GET.get('status')
    nome = list(Filme.objects.all())
    id_usuario = request.session.get('usuario')
    return render(request, 'filmes.html', {
        "status": status, 
        "nome":nome,
        "banner": random.choice(MELHORES_BANNERS),
        "id_user": id_usuario
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

def pegaElencoIndicado(nomeacao):
    todos = list(Elenco.objects.all().filter(nomeAtor=nomeacao.responsavel))
    retorno = None
    if len(todos) > 0:
        for i in todos:
            if i.id_filme == nomeacao.id_filme:
                retorno = i
                break
    return retorno


def pegaNomeacoes(id_filme):
    todos = list(Nomination.objects.all().filter(id_filme=id_filme))
    if len(todos) > 0:
        return todos;
    else:
        return []

def pegaNomeacaoId(id_nomeacao):
    todos = list(Nomination.objects.all().filter(id=id_nomeacao))
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
    id_usuario = request.session.get('usuario')
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
        "estadoTomatoe":pegaEstadoTomatoe(aux.tomatoes),
        "id_user": id_usuario
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
            {
                'Nomeacao': i,
                'Filme': pegaFilme(id_filme=i.id_filme)
            }
        )
    return {
        "CategoriaE": categoria,
        "Categoria": CATEGORIAS[buscaCategoriaPortugues(categoria)],
        "Indicados": retorno
    }

def pegaCategoriasPT():
    portu = []
    for i in CATEGORIAS:
        portu.append(i[1])
    return portu

def pegaTodosIndicados():
    todos = []
    for i in CATEGORIAS:
        todos.append(
            pegaCategoria(i[0])
        )
    return todos