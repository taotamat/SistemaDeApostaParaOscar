from ast import Sub
from django.http import HttpResponse
from django.shortcuts import render
from .models import Administrador
from django.shortcuts import redirect
from filmes.views import CATEGORIAS, pegaFilme, pegaTodosIndicados, pegaNomeacaoId
from filmes.models import Filme, Banner, Elenco, Nomination
from apostas.models import Aposta, Resultado
from usuarios.models import Notificacao, Usuario, Acerto

import usuarios.views as usuaV
from apostas.views import pegaAposta, pegaTodasApostasCat, pegaPremio

import abc


class Observer():

    # Aquele que anunciará quem ganhará

    def __init__(self, vencedor=None, categoria=None):
        self._anunciado = False
        self._vencedor = vencedor
        self._categoria = categoria
        self._contatos = []

    @property
    def anunciado(self):
        return self._anunciado

    @property
    def vencedor(self):
        return self._vencedor

    @property
    def categoria(self):
        return self._categoria

    @anunciado.setter
    def anunciado(self,i):
        self._anunciado = i

    @vencedor.setter
    def vencedor(self,i):
        self._vencedor = i
    
    @categoria.setter
    def categoria(self,i):
        self._categoria = i

    @property
    def contatos(self):
        return self._contatos
    
    @contatos.setter
    def contatos(self,a):
        self._contatos = a



    def anunciar(self, id_nomeacao):
        self.vencedor = id_nomeacao

    def adicionar(self, contato):
        self.contatos.append(contato)

    def avisarAcertos(self):
        mensagem = 'Acesse seu resultados pra saber o seu placar!'
        titulo = 'Todos os resultados sairam!'
        notificarTodos(mensagem, titulo)


        """ acertos = []
        for i in self.contatos:
            if i.id_nomeacao == self.vencedor:
                categoria = list(Nomination.objects.all().filter(id=i.id_nomeacao))[0]
                titulo = f'Você acertou a categoria de {categoria.categoria}!!!'
                mensagem = f'O resultado da categoria que você apostou saiu e você pontuou.'
                i.notificarC(titulo=titulo, mensagem=mensagem)
                acertos.append(i)
        return acertos """

class Contato():
    
    def __init__(self, id_usuario=None, id_nomeacao=None, categoria=None):
        self._id_usuario = id_usuario
        self._id_nomeacao = id_nomeacao
        self._categoria = categoria

    @property
    def id_usuario(self):
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self,i):
        self._id_usuario = i

    @property
    def id_nomeacao(self):
        return self._id_nomeacao

    @id_nomeacao.setter
    def id_nomeacao(self,i):
        self.id_nomeacao = i

    @property
    def categoria(self):
        return self._categoria


    @categoria.setter
    def categoria(self,i):
        self._categoria = i

    def notificarC(self, titulo, mensagem):
        notificar(self.id_usuario, mensagem, titulo)

class TemplateMethod(abc.ABC):
    
    def construirAnuncio(self):
        self.adicionarContatos()
        self.anunciarVencedor()
        self.notificarVencedores()
        self.atualizaAcertos()
    
    @abc.abstractclassmethod
    def adicionarContatos(self):
        pass
    
    @abc.abstractclassmethod
    def anunciarVencedor(self):
        pass
    
    @abc.abstractclassmethod
    def notificarVencedores(self):
        pass

    @abc.abstractclassmethod
    def atualizaAcertos(self):
        pass

class Subclasse(TemplateMethod):
    
    def __init__(self, vencedor, categoria):
        self._categoria = categoria
        self._vencedor = vencedor #........ Filme vencedor da categoria; id da nomeacao
        self._acertos = [] #............... Apostas q acertaram
        self._observador = Observer()
        self._todas = [] # 
    
    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self,i):
        self._categoria = i
    
    @property
    def vencedor(self):
        return self._vencedor

    @vencedor.setter
    def vencedor(self,i):
        self._vencedor = i

    @property
    def acertos(self):
        return self._acertos

    @acertos.setter
    def acertos(self,i):
        self._acertos = i

    @property
    def observador(self):
        return self._observador

    @observador.setter
    def observador(self,i):
        self._observador = i

    @property
    def todas(self):
        return self._todas

    @todas.setter
    def todas(self,i):
        self._todas = i


    # ------------------------PASSOS------------------------------ #

    def adicionarContatos(self):
        self.todas = pegaTodasApostasCat(self.categoria) # Pega todas as apostas feitas por todos os usuários para tal categoria
        for i in self.todas:
            novo = Contato(i.id_usuario, i.pos1, self.categoria)
            self.observador.adicionar(novo) # Adiocina todos os contatos no observador

    def anunciarVencedor(self):
        # And the Oscar Goes To...
        self.observador.anunciar(self.vencedor)

    def notificarVencedores(self):
        self.acertos = self.observador.avisarAcertos()

    def buscaAposta(self, id_aposta):
        for i in self.todas:
            if i.id == id_aposta:
                return i
        return None

    def atualizaAcertos(self):
        aux = self.acertos
        for i in aux:
            a = pegaAcerto(i.id_usuario)
            apo = list(Aposta.objects.all().filter(id_usuario=i.id_usuario).filter(categoria=i.categoria))
            atuAcerto(a, i.categoria, self.vencedor, apo)
            a.save()

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

    aux = list(Resultado.objects.all())
    if len(aux) == 23:
        anunciar()


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

def valida_notificacao(request):
    usuarios = request.POST.get(f'selecionado')
    titulo = request.POST.get('titulo')
    mensagem = request.POST.get('mensagem')


    if usuarios == None or titulo == '':
        return redirect('/administrador/notificaA/?status=1')
    else:
        if usuarios == '-1':
            notificarTodos(mensagem, titulo)
        else:
            notificar(id_user=int(usuarios), mensagem=mensagem, titulo=titulo)
        
        return redirect('/administrador/notificaA/?status=0')

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

def anunciarVencedores(request):
    id_a = request.session.get('administrador')
    status = request.GET.get('status')
    anunciar()
    return render(request, 'anuncio.html', {
        'status': status,
        'id_admin': id_a
        }
    )

def devolvePos(a):
    return [
        a.pos1,
        a.pos2,
        a.pos3,
        a.pos4,
        a.pos5,
        a.pos6,
        a.pos7,
        a.pos8,
        a.pos9,
        a.pos10 ]

def pegaAcerto(id_usuario):
    a = list(Acerto.objects.all().filter(id_usuario=id_usuario) )
    if len(a) > 0:
        return a[0]
    else:
        return None

def atuAcerto(a, categoria, id_vencedor, apos):
    porcentagens = [90, 50, 0, -50, -90] if categoria == 'Best Picture ' else [90, 60, 40, 20, 0, 0, -20, -40, -60, -90]
    porcentagem = 0

    posis = devolvePos(apos)
    k = 0


    for i in posis:
        if id_vencedor == i:
            porcentagem = k
            break
        k += 1
    

    premio = pegaPremio(porcentagens[porcentagem], apos.valor)

    if porcentagem == 0:
        a.catAcertadas += 1

    if premio[0] > 0 and premio[1] > 0:

        if premio[0] != 0:
            # Usuário não errou feio e ainda vai ganhar.
            a.valorGanho = a.valorGanho + premio[0]
        else:
            # Usuário errou feio e ainda perder saldo.
            a.valorPerdido = a.valorPerdido - premio[1]
    
    a.save()
    return porcentagem

def resultarAposta(aposta, categoria, resultado):
    porcentagens = [90, 50, 0, -50, -90] if categoria != 'Best Picture ' else [90, 60, 40, 20, 0, 0, -20, -40, -60, -90]
    porcentagem = 0

    posis = devolvePos(aposta)
    
    k = 0
    for i in posis:
        if resultado.id_indicado.id == i:
            porcentagem = k
            break
        k += 1

    premio = pegaPremio(porcentagens[porcentagem], aposta.valor)

    a = list(Acerto.objects.all().filter(id_usuario=aposta.id_usuario))[0]
    a.valorTotalApostado = a.valorTotalApostado + aposta.valor

    acertou = 0    

    if resultado.id_indicado.id == aposta.pos1:
        # O usuário acertou!!!
        a.catAcertadas += 1
        acertou = 1
    
    a.valorGanho = a.valorGanho + premio[0]
    a.valorPerdido = a.valorPerdido + premio[1]

    a.save()
    return acertou

def anunciar():
    #usuarios = list(Usuario.objects.all())
    for i in CATEGORIAS:

        res = list(Resultado.objects.all().filter(categoria=i[0]))[0] # Pego os resultados do banco de dados.
        apos = list(Aposta.objects.all().filter(categoria=i[0]))

        for j in apos:
            aux = resultarAposta(j, i[0], res)
            if aux == 1:
                feedb = {
                    'titulo': f'Você acertou a categoria de {i[1]}',
                    'mensagem': f'Abra a seção resultados para verificas todos os resultados!'
                }
                notificar(j.id_usuario, feedb['mensagem'], feedb['titulo'])


        



        
        
        
        
        
        """ andTheOscarGoesTo = Subclasse(vencedor=r.id_indicado.id, categoria=r.categoria)
        andTheOscarGoesTo.construirAnuncio() """