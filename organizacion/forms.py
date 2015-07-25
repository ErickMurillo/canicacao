# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class Comercializacion_OrgForm(ModelForm):
	fecha = forms.IntegerField(label='Año de recolección de información',widget=forms.TextInput(attrs={'placeholder': 'Ej: 2015'}))

	class Meta:
		model = Comercializacion_Org
		fields = ('fecha','cacao_baba_acopiado','cacao_seco_comercializado','socios_cacao','productores_no_asociados',
					'tipo_producto','tipo_mercado','destino_produccion')