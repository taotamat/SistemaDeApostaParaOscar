from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.shortcuts import redirect
from hashlib import sha256


def perfil(request):
    status = request.GET.get('status')

    id_usuario = request.session.get('usuario')
    usuario = Usuario.objects.filter(id=id_usuario)[0]

    return render(request, 'perfil.html', {
        'status': status,
        'nome': usuario.nome,
        'id_user': usuario.id
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
            senha = sha256(senha.encode()).hexdigest()
            usuario = Usuario(nome=nome, senha=senha, email=email)
            usuario.save()
            retorno = redirect('/auth/cadastro/?status=0')
        except:
            retorno = redirect('/auth/cadastro/?status=4')

    return retorno

def valida_login(request):

    email = request.POST.get('email')
    senha = request.POST.get('senha')
    senha = sha256(senha.encode()).hexdigest()

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




# ---------#---------#------- #-