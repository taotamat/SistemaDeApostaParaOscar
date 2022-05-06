from .views import notificar


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
        acertos = []
        for i in self._contatos:
            if i.id_filme == self.vencedor:
                titulo = f'Você acertou a categoria de {self.categoria}!!!'
                mensagem = f'O resultado da categoria que você apostou saiu e você pontuou.'
                notificar(id_user, mensagem, titulo)
        return acertos


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

    def notificar(self, titulo, mensagem):
        notificar(self.id_user, mensagem, titulo)

