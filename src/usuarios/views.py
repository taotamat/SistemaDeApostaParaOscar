from django.shortcuts import render
from django.http import HttpResponse

from administrador.views import busca_notifica, pegaAcerto
from .models import Usuario, Notificacao, Acerto
from apostas.models import Aposta, Resultado
from django.shortcuts import redirect
from hashlib import sha256
#from administrador.views import notificar, notificarTodos, busca_notifica
from apostas.views import pegaPremio

def perfil(request):
    status = request.GET.get('status')

    id_usuario = request.session.get('usuario')
    usuario = Usuario.objects.filter(id=id_usuario)[0]

    a = pegaAcerto(id_usuario)
    a.valorTotalApostado = round(a.valorTotalApostado, 2)
    a.save()

    res = list(Resultado.objects.all())

    return render(request, 'perfil.html', {
        'status': status,
        'nome': usuario.nome,
        'id_user': usuario.id,
        'usuario': usuario,
        'acerto': a,
        'total': len(res)
        }
    )

def login(request):
    status = request.GET.get('status')
    return render(request, 'login.html', {
        'status': status,
        'id_user': None
        }
    )

def cadastro(request):
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {
        'status': status,
        'id_user': None
        }
    )

def sair(request):
    request.session["usuario"] = None
    return redirect('/auth/login/')

def mudar_senha(request):
    status = request.GET.get('status')
    return render(request, 'mudar_senha.html', {
        'status': status,
        'id_user': None
        }
    )

def mudarDados(request):
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    usuario = Usuario.objects.filter(id=id_usuario)[0]
    senha = usuario.senha
    return render(request, 'mudarDados.html', {
        'status': status,
        'nomeUser': usuario.nome,
        'emailUser': usuario.email,
        'senhaUser': sha256(usuario.senha.encode()).hexdigest(),
        'id_user': usuario.id
        }
    )

def valida_cadastro(request):

    erro = 1

    nome = request.POST.get('nome')
    senha = request.POST.get('senha')
    email = request.POST.get('email')

    usuario = Usuario.objects.filter(email = email)

    if len(nome.strip()) == 0 or len(email.strip()) == 0:
        retorno = redirect('/auth/cadastro/?status=1')
    elif len(senha) < 8:
        retorno = redirect('/auth/cadastro/?status=2')
    elif len(usuario) > 0:
        retorno = redirect('/auth/cadastro/?status=3')
    else:
        try:
            #senha = sha256(senha.encode()).hexdigest()
            usuario = Usuario(nome=nome, senha=senha, email=email)
            usuario.save()
            erro = 0

            retorno = redirect('/auth/cadastro/?status=0')
        except:
            retorno = redirect('/auth/cadastro/?status=4')

    if erro == 0:
        aux = list(Usuario.objects.all().filter(email=email))
        #notificar(id_user=aux[0].id, mensagem=' ', titulo='Conta cadastrada com sucesso!')
        busca_notifica(aux[0], ' ', f'Conta de {aux[0].nome} criada com sucesso!')
        novo = Acerto(id_usuario=aux[0].id, nome_usuario=aux[0].nome)
        novo.save()

    return retorno

def valida_login(request):

    email = request.POST.get('email')
    senha = request.POST.get('senha')
    #senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email=email).filter(senha=senha)

    if len(usuario) == 0:
        retorno = redirect('/auth/login/?status=1')
    else:
        request.session['usuario'] = Usuario.objects.filter(email=email)[0].id
        retorno = redirect(f'/home/')

    return retorno

def valida_mudanca_senha(request):
    email = request.POST.get('email')
    nova_senha = request.POST.get('nova_senha')
    nova_senha = sha256(nova_senha.encode()).hexdigest()
    usuario = Usuario.objects.filter(email = email)

    if len(email) == 0 or len(nova_senha) == 0:
        # O usuário deixou campos em branco
        retorno = redirect('/auth/mudar_senha/?status=1')

    else:
        usuario = Usuario.objects.filter(email = email)
        retorno = HttpResponse(f'usuario = {len(usuario)}')

        if len(usuario) == 0:
            # O email digitado não foi encontrado!
            retorno = redirect('/auth/mudar_senha/?status=2')
        elif len(nova_senha) < 8:
            # A nova senha deve possuir no minimo 8 caracteres.
            retorno = redirect('/auth/mudar_senha/?status=3')
        else:
            # Senha alterada com sucesso!
            usuario.update(senha=nova_senha)
            retorno = redirect('/auth/login/?status=2')

    return retorno

def alterarDados(request):

    id_usuario = request.session.get('usuario')
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    usuario = Usuario.objects.filter(id=id_usuario)

    if (len(nome)+len(senha)+len(email)) != 0:
        if nome != '':
            usuario.update(nome=nome)
        
        if email != '':
            usuario.update(email=email)
        
        if senha != '':
            nova_senha = sha256(nova_senha.encode()).hexdigest()
            usuario.update(senha=nova_senha)
            
        
        usuario.update(id=id_usuario)
        s = 1

    else:
        s = 2


    return redirect(f'/auth/mudarDados/?status={s}')

def pegaUser(id_user):
    todos = list(Usuario.objects.all().filter(id=id_user))
    if len(todos) == 0:
        return None
    else:
        return todos[0]

def pegaNotificacoes(id_user):
    id_usuario = int(id_user)
    todos = list(Notificacao.objects.all().filter(id_usuario=id_usuario))
    if len(todos) == 0:
        return None
    else:
        return todos

def notificacoes(request):
    
    status = request.GET.get('status')
    id_usuario = request.session.get('usuario')
    n = pegaNotificacoes(id_user=id_usuario)

    if n != None:
        n = list(reversed(n))

    return render(request, 'notificacoes.html', {
        'status': status,
        'id_user': id_usuario,
        'notificacoes': n
        }
    )

""" def buscaPlacarAux(id_usuario):

    apostas = list(Aposta.objects.all().filter(id_usuario=id_usuario))

    retorno = {
        'qnt_cats_apostadas': len(apostas)
    }

    for i in apostas:
        res = list(Resultado.objects.all().filter(categoria=i.categoria).filter(id_usuario=id_usuario))[0]

        if i.categoria != 'Best Picture ': """




# ---------#---------#------- #-