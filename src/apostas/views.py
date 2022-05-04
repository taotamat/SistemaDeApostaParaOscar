from urllib.parse import urlencode
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from apostas.forms import *
from filmes.views import pegaElencoIndicado, pegaElenco, pegaFilme, pegaNomeacaoId, pegaBanner, pegaCategoria, pegaCategoriasPT, CATEGORIAS, MELHORES_BANNERS
from .models import Resultado, Aposta
import random
from datetime import datetime
from administrador.views import notificar, notificarTodos, busca_notifica
import math

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

    valor = request.POST.get('valor')

    tudo = []
    for i in range(1, qnt+1):
        tudo.append(
            {
                'posicao': i,
                'id_nomeado': request.POST.get(f'pos_{i}')
            }
        )  

    retorno = None

    for aux in tudo:
        if '' == aux['id_nomeado']:
            return redirect(f'/apostas/montar/%3FP{categoria[0:len(categoria)-1]}%20%5B-a-zA-Z0-9_%5D+)%5CZ/?status=1')
    

    for j in tudo:
        if int(j['id_nomeado']) < 1 or int(j['id_nomeado']) > qnt:
            return redirect(f'/apostas/montar/%3FP{categoria[0:len(categoria)-1]}%20%5B-a-zA-Z0-9_%5D+)%5CZ/?status=2')
    

    for k in range(1, qnt+1):
        achou = 0
        for j in tudo:
            if int(j['id_nomeado']) == k:
                achou += 1
            
            if achou == 2:
                return redirect(f'/apostas/montar/%3FP{categoria[0:len(categoria)-1]}%20%5B-a-zA-Z0-9_%5D+)%5CZ/?status=3')


    if retorno == None:
        request.session['aposta'] = {'categoria': categoria, 'posicoes':tudo, 'qnt': qnt, 'valor': float(valor)}
        return redirect(f'/apostas/finalizar/')

def pegaPremio(porcentagem, valor):
    premio = []

    if porcentagem > 0:
        premio.append( round((abs(porcentagem) / 100) * valor, 2) )
        premio.append( round(float(0), 2) )

    elif porcentagem < 0:
        premio.append( round(float(0), 2) )
        premio.append(round((abs(porcentagem) / 100) * valor, 2))

    else:
        premio.append( round(float(0), 2) )
        premio.append( round(float(0), 2) )

    return premio


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

    valor = aposta['valor']
    porcentagens = [90, 50, 0, -50, -90] if aposta['qnt'] == 5 else [90, 60, 40, 20, 0, 0, -20, -40, -60, -90]

    for j in range(1, int(aposta['qnt'])+1):
        busca = True
        k = 0
        while( busca == True and k < int(aposta['qnt'])):
            if int(aposta['posicoes'][k]['posicao']) == j:
                ordenados.append(novo[k])
                # (-20) / 100 * 50
                # """ += ( (porcentagens[k] / 100) * float(aposta['valor']) ) """
                ordenados[k]['premio'] = pegaPremio(porcentagens[k], valor) 
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

def organizaAposta(indicados, aposta):
    organizado = []
    for i in aposta['posicoes']:
        organizado.append( indicados[ int(i['id_nomeado']) - 1 ]['Nomeacao'] )
    return organizado

def salvaAposta(request):
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    indicados = request.session.get('indicados')
    aposta = [request.session.get('aposta')]

    try:
        organizacao = organizaAposta(indicados, aposta[0])

        if aposta[0]['qnt'] == 5:
            for j in range(5):
                organizacao.append(0)

        nova = Aposta(
            id_usuario = id_usuario,
            categoria = aposta[0]['categoria'],
            valor = aposta[0]['valor'],
            dataA = datetime.now(),
            pos1 = organizacao[0],
            pos2 = organizacao[1],
            pos3 = organizacao[2],
            pos4 = organizacao[3],
            pos5 = organizacao[4],
            pos6 = organizacao[5],
            pos7 = organizacao[6],
            pos8 = organizacao[7],
            pos9 = organizacao[8],
            pos10 = organizacao[9]
        )

    except:
        return redirect('/apostas/finalizar/?status=1')
    
    
    nova.save()
    notificar(id_usuario, f'Aposta da categoria {aposta[0]["categoria"]} foi cadastrada com sucesso, aguarde os resultados!', 'Aposta cadastrada com sucesso!')
    return redirect('/apostas/finalizar/?status=0')

