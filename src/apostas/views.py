from urllib.parse import urlencode
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from apostas.forms import *
from filmes.views import pegaElencoIndicado, pegaElenco, pegaFilme, pegaNomeacaoId, pegaBanner, pegaCategoria, pegaCategoriasPT, CATEGORIAS, MELHORES_BANNERS
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


def ehAtor(categoria):
    retorno = False
    for i in ['Actor ', 'Actress ', 'Supporting Actor ', 'Supporting Actress ']:
        if categoria == i:
            retorno = True
            break
    return retorno


def acrescentaIMG(indicados, categoria):
    ator = ehAtor(categoria)
    k = 1
    for i in indicados:
        if ator == True:
            i['imagem'] = pegaElencoIndicado(i['Nomeacao'])
            i['Ator'] = 1
            

        else:
            i['imagem'] = i['Filme'].poster
            i['Ator'] = 0

        i['posicao'] = f'pos_{k}'

        k += 1

    #indicados['posicao'] = [ (f'pos_{x}') for x in range(1, 11) ]

    return indicados


def ajustaSessionIndicados(indicados):
    retorno = []
    for i in indicados:
        novo = {
            "Nomeacao": i['Nomeacao'].id,
            "Filme": i['Filme'].id,
            "Ator": i["Ator"]
        }

        if i["Ator"] == 1:
            novo["Imagem"] = i['imagem'].imagem
            novo['Elenco'] = i['imagem'].id
        else:
            novo["Imagem"] = i["imagem"]
            novo['Elenco'] = None
        
        retorno.append(novo)
    
    return retorno



def montar(request, categoria):
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    c = pegaCategoria(categoria)

    c['Indicados'] = acrescentaIMG(c['Indicados'], categoria)
    
    #request.session['indicados'] = [ i['Nomeacao'].id for i in c['Indicados'] ]

    request.session['indicados'] = ajustaSessionIndicados(c['Indicados'])    

    return render(request, 'aposta2.html', {
        'status': status, 
        'id_user':id_usuario,
        'categoria': c['Categoria'],
        'indicados': c['Indicados'],
        'c': c
        }
    )

    """ status = request.GET.get('status')
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
    ) """


def resultados(request):
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    resultadosL = list(Resultado.objects.all())

    filmes = []
    
    indicacoes = []

    for i in resultadosL:
        nomeacao = pegaNomeacaoId(i.id_indicado.id)
        if len(nomeacao) > 0:
            indicacoes.append(nomeacao[0])
    
    for j in indicacoes:
        f = pegaFilme(j.id_filme)
        if j.categoria in ['Actor ', 'Actress ', 'Supporting Actor ', 'Supporting Actress ']:
            indicado = {'indicado': pegaElencoIndicado(j), 'categoria': j.categoria, 'ator':1, 'filme': f,'responsavel':j.responsavel}
        else:
            indicado = {'indicado': f, 'categoria': j.categoria, 'ator':0, 'filme': f, 'responsavel':j.responsavel}
        filmes.append(indicado)

    return render(request, 'resultados.html', {
        'status': status, 
        'id_user':id_usuario,
        'categoriasTodas': CATEGORIAS,
        "banner": random.choice(MELHORES_BANNERS),
        'temResultados':len(resultadosL),
        'resultadosL': filmes
        }
    )

def verificar(request, categoria):
    qnt = 10 if categoria == 'Best Picture ' else 5

    tudo = []
    for i in range(1, qnt+1):
        tudo.append(request.POST.get(f'pos_{i}'))

    retorno = None

    if '' in tudo:
        return redirect(f'/apostas/montar/%3FP{categoria[0:len(categoria)-1]}%20%5B-a-zA-Z0-9_%5D+)%5CZ/?status=1')
    

    for j in tudo:
        if int(j) < 1 or int(j) > qnt:
            return redirect(f'/apostas/montar/%3FP{categoria[0:len(categoria)-1]}%20%5B-a-zA-Z0-9_%5D+)%5CZ/?status=2')
    

    for k in range(1, qnt+1):
        achou = 0
        for j in tudo:
            if int(j) == k:
                achou += 1
            
            if achou == 2:
                return redirect(f'/apostas/montar/%3FP{categoria[0:len(categoria)-1]}%20%5B-a-zA-Z0-9_%5D+)%5CZ/?status=3')


    if retorno == None:
        request.session['aposta'] = {'categoria': categoria, 'posicoes':tudo, 'qnt': qnt}
        return redirect(f'/apostas/finalizar/')

def finalizar(request):
    status = request.GET.get('status')
    aposta = request.session.get('aposta')
    id_usuario = request.session.get('usuario')
    indicados = request.session.get('indicados')

    novo = []

    for i in indicados:
        item = {
            'Filme': pegaFilme(i['Filme']),
            'Nomeacao': pegaNomeacaoId(i['Nomeacao'])
        }

        if i['Ator'] == 1:
            item['imagem'] = i['Imagem']
            item['ator'] = i['Ator']
            item['elenco'] = pegaElencoIndicado(item['Nomeacao'][0])
        else:
            item['imagem'] = i['Imagem']
            item['ator'] = i['Ator']
            item['elenco'] = None

        novo.append(item)
    

    ordenados = []

    for j in range(1, int(aposta['qnt'])+1):
        busca = True
        k = 0
        while( busca == True and k < int(aposta['qnt'])):
            if int(aposta['posicoes'][k]) == j:
                ordenados.append(novo[k])
                busca = False
            k += 1


    return render(request, 'finalizar.html', {
        'status': status, 
        'id_user': id_usuario,
        'aposta': aposta,
        'novo': indicados,
        'indicados': ordenados
        }
    )



    #return HttpResponse(f"categoria: {aposta['categoria']}\nposicoes: {aposta['posicoes']}\nqnt: {aposta['qnt']} ")