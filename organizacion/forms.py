# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

def departamentos():   
	foo = Encuesta_Org.objects.all().order_by('organizacion__municipio__departamento__nombre').distinct().values_list('organizacion__municipio__departamento__id', flat=True)
	return Departamento.objects.filter(id__in=foo)

class OrganizacionConsulta(forms.Form):
	def __init__(self, *args, **kwargs):
		super(OrganizacionConsulta, self).__init__(*args, **kwargs)
		self.fields['departamento'] = forms.ModelMultipleChoiceField(queryset=departamentos(), required=True, label=u'Departamentos')
		self.fields['municipio'] = forms.ModelMultipleChoiceField(queryset=Municipio.objects.all().order_by('nombre'), required=True)
		self.fields['comunidad'] = forms.ModelMultipleChoiceField(queryset=Comunidad.objects.all(), required=False)