from curses import def_prog_mode
from django.db import models

# Create your models here.





class Filme(models.Model):
    
    nome = models.CharField(max_length=100)
    poster = models.URLField(default='')
    
    ava_imdb = models.FloatField(default=0.0)
    ava_letter = models.FloatField(default=0.0)
    ava_tmdb = models.IntegerField(default=0)

    sinopse = models.TextField(default='')
    ano = models.IntegerField(default=2021)
    diretor = models.CharField(max_length=100, default='')

    ondeAssistirLink = models.URLField(default='')
    ondeAssistirImg = models.URLField(default='')
    servico = models.CharField(max_length=100, default='')

    genero = models.CharField(max_length=100, default='')
    duracao = models.CharField(max_length=100, default='')

    link_letter = models.URLField(default='')
    link_imdb = models.URLField(default='')
    link_tmdb = models.URLField(default='')
    link_tomatoes = models.URLField(default='')

    tomatoes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.nome



class Banner(models.Model):

    id_filme = models.IntegerField()
    banner = models.URLField(default='')

    def __int__(self) -> int:
        return self.id_filme


class Elenco(models.Model):

    nomeAtor = models.CharField(max_length=100)
    nomePersonagem = models.CharField(max_length=100)
    id_filme = models.IntegerField()
    link_tmdb = models.URLField(default='')
    imagem = models.URLField(default='')

    def __str__(self) -> str:
        return self.nomeAtor


class Nomination(models.Model):

    categoria = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100)
    id_filme = models.IntegerField()

    def __str__(self) -> str:
        return self.categoria
