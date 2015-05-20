# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class Uso_TierraForm(ModelForm):

    class Meta:
        model = Uso_Tierra

    def clean(self):
        area_total = self.cleaned_data.get('area_total')
        bosque = self.cleaned_data.get('bosque')
        tacotal = self.cleaned_data.get('tacotal')
        cultivo_anual = self.cleaned_data.get('cultivo_anual')
        plantacion_forestal = self.cleaned_data.get('plantacion_forestal')
        area_pasto_abierto = self.cleaned_data.get('area_pasto_abierto')
        area_pasto_arboles = self.cleaned_data.get('area_pasto_arboles')
        cultivo_perenne = self.cleaned_data.get('cultivo_perenne')
        cultivo_semi_perenne = self.cleaned_data.get('cultivo_semi_perenne')
        cacao = self.cleaned_data.get('cacao')
        huerto_mixto_cacao = self.cleaned_data.get('huerto_mixto_cacao')

        suma_total = (bosque + tacotal + cultivo_anual + plantacion_forestal + area_pasto_abierto + area_pasto_arboles
                    + cultivo_perenne + cultivo_semi_perenne + cacao + huerto_mixto_cacao)

        if (area_total < suma_total):

            raise ValidationError("Distribución de finca mayor al área total")

        return self.cleaned_data