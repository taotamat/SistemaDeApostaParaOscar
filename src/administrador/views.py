from django.http import HttpResponse
from django.shortcuts import render
from .models import Administrador
from django.shortcuts import redirect
from filmes.views import CATEGORIAS, pegaFilme, pegaTodosIndicados, pegaNomeacaoId
from filmes.models import Filme, Banner, Elenco, Nomination
from apostas.models import Aposta, Resultado
from usuarios.models import Notificacao, Usuario


# Create your views here.
def administrador(request):

    logado = request.session.get('administrador')

    if logado != None:
        request.session["administrador"] = None

    status = request.GET.get('status')
    return render(request, 'loginA.html', {
        'status': status
        }
    )

def valida_loginA(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    a = Administrador.objects.filter(email=email).filter(senha=senha)

    if len(a) == 0:
        return redirect('/administrador/login/?status=1')
    else:
        request.session['administrador'] = Administrador.objects.filter(email=email)[0].id
        return redirect(f'/administrador/home/')

def home(request):
    id_a = request.session.get('administrador')
    status = request.GET.get('status')
    return render(request, 'menuA.html', {
        'status': status,
        'id_admin': id_a
        }
    )

def taCats(categoria, cats):
    retorno = False
    for i in cats:
        if categoria[0] == i:
            retorno = True
            break
    return retorno


def cadResultados(request):
    indicados = pegaTodosIndicados()
    aux = list(Resultado.objects.all())

    cats = []
    ainda = []

    if len(aux) == 23:
        # Todas as categorias já foram cadastradas!
        return redirect('/administrador/cadResultados/?status=1')
    
    if len(aux) != 0:
        for i in aux:
            # For q vai me dizer quais categorias já possuem resultados
            cats.append(i.categoria)
    
    k = 0
    for j in indicados:
        if len(cats) == 0 or (taCats(j['Categoria'], cats) != True):
            ainda.append(j)
            
        
    status = request.GET.get('status')
    id_a = request.session.get('administrador')
    return render(request, 'cadResultados.html', {
        'status': status,
        'id_admin': id_a,
        'indicados': ainda
        }
    )
    
def valida_resultados(request):

    """ 
        Fazer:
            - Padrões de projeto
            - Edição de resultado
            - Edição de apostas para o usuário
            - Comparação das apostas com resultado. Colocar template method aqui.
            - Acertos (Acho q isso pode ser no perfil) [ referente a quais categorias o usuario acertou e valor total]
            - Editar pra mostrar quais categorias já foram apostadas 
    """



    Todas = []

    for i in CATEGORIAS:
        id_nomeado = request.POST.get(f'{i[0]}')
        if id_nomeado != None:
            Todas.append(
                {
                    'categoria': i,
                    'id_indicado': request.POST.get(f'{i[0]}')
                }
            )
    
    salvar_resultados(Todas)

    #return HttpResponse(Todas)

    selecionados = []
    for j in Todas:
        n = pegaNomeacaoId(int(j['id_indicado']))[0] 
        selecionados.append(
            {
                'nomeacao': n,
                'filme': pegaFilme(n.id_filme)
            }
        )

    id_a = request.session.get('administrador')
    status = request.GET.get('status')
    return render(request, 'resultados_salvos.html', {
        'status': status,
        'id_admin': id_a,
        'selecionados': selecionados
        }
    )

def salvar_resultados(tudo):
    for i in tudo:
        n = pegaNomeacaoId(int(i['id_indicado']))
        r = Resultado(categoria=i['categoria'][0], id_indicado=n[0])
        r.save()

def sairA(request):
    request.session["administrador"] = None
    return redirect('/administrador/')

def notificar(id_user, mensagem, titulo):
    n = Notificacao(titulo=titulo, mensagem=mensagem, id_usuario=id_user)
    n.save()

def notificarTodos(mensagem, titulo):

    todos = list(Usuario.objects.all())

    if len(todos) > 0:
        for i in todos:
            notificar(i.id, mensagem, titulo)

def busca_notifica(usuario, mensagem, titulo):
    notificar(usuario.id, mensagem, titulo)

def notificaA(request):
    id_a = request.session.get('administrador')
    status = request.GET.get('status')
    todos = list(Usuario.objects.all())

    if len(todos) > 0:
        usuarios = [{'nome': 'Todos', 'id_user': -1}]
        for i in todos:
            usuarios.append(
                {
                    'nome': i.nome,
                    'id_user': i.id
                }
            )
    else:
        usuarios = None

    return render(request, 'notificaA.html', {
        'status': status,
        'id_admin': id_a,
        'usuarios': usuarios
        }
    )

def editaResults(request):
    

    indicados = pegaTodosIndicados()
    aux = list(Resultado.objects.all())
    
    qnt = len(aux)

    cats = []
    ainda = []

    if qnt == 23:
        # Todas as categorias já foram cadastradas!
        return redirect('/administrador/editaResults/?status=1')
    
    if qnt != 0:
        for i in aux:
            # For q vai me dizer quais categorias já possuem resultados
            cats.append(i.categoria)
    
    k = 0
    for j in indicados:
        if len(cats) != 0 and (taCats(j['Categoria'], cats) == True):
            ainda.append(j)
    

    status = request.GET.get('status')
    id_a = request.session.get('administrador')
    return render(request, 'ediResultados.html', {
        'status': status,
        'id_admin': id_a,
        'qnt': qnt,
        'indicados': ainda
        }
    )

def valida_edicao_results(request):
    Todas = []

    for i in CATEGORIAS:
        id_nomeado = request.POST.get(f'{i[0]}')
        if id_nomeado != None:
            Todas.append(
                {
                    'categoria': i,
                    'id_indicado': request.POST.get(f'{i[0]}')
                }
            )
    
    salvar_edicao_resultados(Todas)

    selecionados = []
    for j in Todas:
        n = pegaNomeacaoId(int(j['id_indicado']))[0] 
        selecionados.append(
            {
                'nomeacao': n,
                'filme': pegaFilme(n.id_filme)
            }
        )
    
    id_a = request.session.get('administrador')
    status = request.GET.get('status')
    return render(request, 'resultados_salvos.html', {
        'status': status,
        'id_admin': id_a,
        'selecionados': selecionados
        }
    )
    
    

def salvar_edicao_resultados(tudo):
    for i in tudo:
        n = pegaNomeacaoId(int(i['id_indicado']))[0]
        salvo = list(Resultado.objects.all().filter(categoria=i['categoria'][0]))[0]
        salvo.id_usuario = n
        salvo.save()
        #r.save()