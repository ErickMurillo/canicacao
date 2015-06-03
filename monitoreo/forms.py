# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class Uso_TierraForm(ModelForm):

    class Meta:
        model = Uso_Tierra
        fields = ('area_total','bosque','tacotal','cultivo_anual','plantacion_forestal','area_pasto_abierto','area_pasto_arboles',
                    'cultivo_perenne','cultivo_semi_perenne','cacao','huerto_mixto_cacao')

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

class EducacionForm(ModelForm):

    class Meta:
        model = Educacion
        fields = ('rango','numero_total','no_lee_ni_escribe','primaria_incompleta','primaria_completa','secundaria_incompleta',
                    'bachiller','universitario_tecnico','viven_fuera')

    def clean(self):
        numero_total = self.cleaned_data.get('numero_total')
        no_lee_ni_escribe = self.cleaned_data.get('no_lee_ni_escribe')
        primaria_incompleta = self.cleaned_data.get('primaria_incompleta')
        primaria_completa = self.cleaned_data.get('primaria_completa')
        secundaria_incompleta = self.cleaned_data.get('secundaria_incompleta')
        bachiller = self.cleaned_data.get('bachiller')
        universitario_tecnico = self.cleaned_data.get('universitario_tecnico')
        viven_fuera = self.cleaned_data.get('viven_fuera')

        suma_total = (no_lee_ni_escribe + primaria_incompleta + primaria_completa + secundaria_incompleta
                    + bachiller + universitario_tecnico + viven_fuera)

        if (numero_total < suma_total):

            raise ValidationError("Distribución de Miembros de Familia mayor al número total")

        return self.cleaned_data