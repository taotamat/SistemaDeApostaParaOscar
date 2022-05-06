from .views import notificar
from apostas.views import pegaTodasApostasCat

from filmes.views import CATEGORIAS
from apostas.models import Aposta, Resultado
from usuarios.views import pegaAcerto, atuAcerto
from usuarios.models import Usuario, Notificacao, Acerto

import abc
from observer import Observer, Contato


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

    def anunciarVencedores(self):
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
        for i in self.acertos:
            a = pegaAcerto(i.id_usuario)
            atuAcerto(a, i.categoria, self.vencedor)

