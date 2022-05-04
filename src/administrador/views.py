from django.http import HttpResponse
from django.shortcuts import render
from .models import Administrador
from django.shortcuts import redirect
from filmes.views import pegaFilme, pegaTodosIndicados
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

def cadResultados(request):
    indicados = pegaTodosIndicados()
    status = request.GET.get('status')
    id_a = request.session.get('administrador')
    return render(request, 'cadResultados.html', {
        'status': status,
        'id_admin': id_a,
        'indicados': indicados
        }
    )
    
def valida_resultados(request):

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




