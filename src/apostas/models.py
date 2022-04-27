from django.db import models
from datetime import datetime

# Create your models here.
# Create your models here.
class Aposta(models.Model):

    id_usuario = models.IntegerField(default=-1)
    categoria = models.CharField(max_length=100)
    pos1 = models.IntegerField(default=-1)
    pos2 = models.IntegerField(default=-1)
    pos3 = models.IntegerField(default=-1)
    pos4 = models.IntegerField(default=-1)
    pos5 = models.IntegerField(default=-1)
    pos6 = models.IntegerField(default=-1)
    pos7 = models.IntegerField(default=-1)
    pos8 = models.IntegerField(default=-1)
    pos9 = models.IntegerField(default=-1)
    pos10 = models.IntegerField(default=-1)

    valor = models.FloatField(default=0.0)
    dataA = models.DateTimeField(blank=True, null=True)


    def __str__(self) -> str:
        return self.categoria


class Resultado(models.Model):
    categoria = models.CharField(max_length=100)
    id_indicado = models.IntegerField(default=-1) # Indicado vencedor

    def __str__(self) -> str:
        return self.categoria