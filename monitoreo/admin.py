# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *

# Register your models here.

class EncuestaAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		if request.user.is_superuser:
			return Encuesta.objects.all()
		return Encuesta.objects.filter(usuario=request.user)

	def save_model(self, request, obj, form, change):
		obj.usuario = request.user
		obj.save()

	exclude = ('usuario',)
	fieldsets = [
		(('Informacion Básica'), {'fields' : (('fecha','recolector','organizacion'),('nombre','cedula','fecha_nacimiento',)
			,('sexo','profesion','nombre_finca'),('departamento','municipio','comunidad'),('latitud','longitud')
			)}),
	]
	list_display = ('nombre','organizacion','recolector','departamento','municipio')
	list_display_links = ('organizacion','nombre')
	list_filter = ('departamento',)
	
admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(Organizaciones)
admin.site.register(Recolector)
