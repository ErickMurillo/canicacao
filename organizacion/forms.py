# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class OrganizacionConsulta(forms.Form):
    departamento = forms.ModelMultipleChoiceField(queryset=Departamento.objects.all().order_by('nombre'), required=True, label=u'Departamentos')
    municipio = forms.ModelMultipleChoiceField(queryset=Municipio.objects.all().order_by('nombre'), required=True)
    comunidad = forms.ModelMultipleChoiceField(queryset=Comunidad.objects.all(), required=False)