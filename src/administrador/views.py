from django.http import HttpResponse
from django.shortcuts import render
from .models import Administrador
from django.shortcuts import redirect
from filmes.views import CATEGORIAS, pegaFilme, pegaTodosIndicados
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
    
    if len(aux) != 0:
        for i in aux:
            # For q vai me dizer quais categorias já possuem resultados
            cats.append(i.categoria)
    
    k = 0
    for j in indicados:
        if len(cats) != 0 and (taCats(j['Categoria'], cats) == True):
            ainda.append(j['oi'])
            
        
    status = request.GET.get('status')
    id_a = request.session.get('administrador')
    return render(request, 'cadResultados.html', {
        'status': status,
        'id_admin': id_a,
        'indicados': indicados
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
        Todas.append( request.POST.get(f'{i[0]}') )

    return HttpResponse(f'{Todas}')

    todos = list(Nomination.objects.all())
    tam = len(todos)
    tudo = []

    for i in range(tam):
        if str(request.POST.get(f'{i}')) == 'True':
            tudo.append(
                {
                    'nomeacao':todos[i],
                    'filme': pegaFilme(todos[i].id_filme)
                }
            )

    #return HttpResponse(f'Olá Mundo! + {filme} + {tam} + {tudo}')

    id_a = request.session.get('administrador')
    status = request.GET.get('status')

    #self.frequencias = sorted(self.frequencias, key=lambda x: x.frequencia)

    tudo = sorted( tudo, key=lambda x: x['nomeacao'].id )

    salvar_resultados(tudo)

    aux = list(Resultado.objects.all())
    if len(aux) == 23:
        notificarTodos(mensagem='Venha comparar seus acertos.', titulo='Resultados cadastrados!')

    return render(request, 'resultados_salvos.html', {
        'status': status,
        'id_admin': id_a,
        'selecionados': tudo
        }
    )

def salvar_resultados(tudo):
    for i in tudo:
        r = Resultado(categoria=i['nomeacao'].categoria, id_indicado=i['nomeacao'])
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


