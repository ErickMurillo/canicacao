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
                    'cultivo_perenne','cultivo_semi_perenne','cacao','huerto_mixto_cacao','otros')

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
        otros = self.cleaned_data.get('otros')

        suma_total = (bosque + tacotal + cultivo_anual + plantacion_forestal + area_pasto_abierto + area_pasto_arboles
                    + cultivo_perenne + cultivo_semi_perenne + cacao + huerto_mixto_cacao + otros)

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

        suma_total = no_lee_ni_escribe + primaria_incompleta + primaria_completa + secundaria_incompleta + bachiller + universitario_tecnico + viven_fuera

        if (numero_total < suma_total):

            raise ValidationError("Distribución de Miembros de Familia mayor al número total")

        return self.cleaned_data

#filtros
def fecha_choice():
    years = []
    for en in Encuesta.objects.order_by('anno').values_list('anno', flat=True):
        years.append((en,en))
    return list(sorted(set(years)))

def departamentos():   
    foo = Encuesta.objects.all().order_by('persona__comunidad__municipio__departamento__nombre').distinct().values_list('persona__comunidad__municipio__departamento__id', flat=True)
    return Departamento.objects.filter(id__in=foo)

SI_NO_CHOICE = (('','----'),(1,'Si'),(2,'No'))

class EncuestaConsulta(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EncuestaConsulta, self).__init__(*args, **kwargs)
        self.fields['anno'] = forms.MultipleChoiceField(choices=fecha_choice(),required=True,label=u'Año')
        self.fields['departamento'] = forms.ModelMultipleChoiceField(queryset=departamentos(), required=False, label=u'Departamentos')
        self.fields['municipio'] = forms.ModelMultipleChoiceField(queryset=Municipio.objects.all().order_by('nombre'), required=False)
        self.fields['comunidad'] = forms.ModelMultipleChoiceField(queryset=Comunidad.objects.all(), required=False)
        self.fields['organizacion'] = forms.ModelMultipleChoiceField(queryset=Organizacion.objects.all(),required=False)
        self.fields['socio'] = forms.ChoiceField(label=u'Socio',choices=SI_NO_CHOICE,required=False)
