""" from cProfile import label
from typing_extensions import Self
from attr import fields """
from django import forms

from apostas.models import Aposta

class Aposta5(forms.ModelForm):
   class Meta:
        model = Aposta

        fields = [
            'pos1',
            'pos2',
            'pos3',
            'pos4',
            'pos5']


        exclude = [
            'id_usuario',
            'pos6',
            'pos7',
            'pos8',
            'pos9',
            'pos10',
            'categoria',
            'valor',
            'dataA'
        ]


   
class Aposta10(forms.ModelForm):
   class Meta:
        model = Aposta

        exclude = [
            'id_usuario',
            'categoria'
        ]    


