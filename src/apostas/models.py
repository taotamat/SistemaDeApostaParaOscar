from django.db import models
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
# Create your models here.
class Aposta(models.Model):

    id_usuario = models.IntegerField(default=0)
    categoria = models.CharField(max_length=100)
    pos1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos2 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos3 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos4 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos5 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos6 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos7 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos8 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos9 = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(10)])
    pos10 = models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(10)])

    valor = models.FloatField(default=0.0)
    dataA = models.DateTimeField(blank=True, null=True)


    def __str__(self) -> str:
        return self.categoria