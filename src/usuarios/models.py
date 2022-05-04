from django.db import models
import django

# Create your models here.
class Usuario(models.Model):

    nome = models.CharField(max_length=30)
    email = models.EmailField()
    senha = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.nome


class Notificacao(models.Model):
    data = models.DateField(default=django.utils.timezone.now)
    titulo = models.CharField(max_length=100)
    mensagem = models.TextField(default='')
    id_usuario = models.IntegerField(default=-1) # -1 é para todos
    vizualizado = models.IntegerField(default=0)
    alertado = models.IntegerField(default=0) # 0 = Não e 1 = Sim;
    tipo = models.IntegerField(default=0) # Variavel q vai informar ao sistema que é uma notificação referente aos resultados!
    # tipo = 1 : é sobre os resultados

    def __str__(self) -> str:
        return self.titulo
