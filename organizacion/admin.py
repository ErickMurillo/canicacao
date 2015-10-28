# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *


# Register your models here.
class Aspectos_JuridicosInline(admin.StackedInline):
	model = Aspectos_Juridicos
	max_num = 1
	can_delete = False
	fieldsets = [
		((None), {'fields' : (('tiene_p_juridica','act_p_juridica','solvencia_tributaria','junta_directiva'),
								('lista_socios','ruc'),('mujeres','hombres'))}),	
	]

class DocumentacionInline(admin.TabularInline):
	model = Documentacion
	max_num = 6
	extra = 1
	can_delete = True

class Datos_ProductivosInline(admin.StackedInline):
	model = Datos_Productivos
	max_num = 1
	can_delete = False
	fieldsets = [
		(('No. de socias/os con cacao'), {'fields' : (('socias','socios'),)}),
		(('No. pre-socias/os con cacao'), {'fields' : (('pre_socias','pre_socios'),)}),
		(('Áreas'), {'fields' : (('area_total','area_cert_organico','area_convencional'),)}),
		(('Rendimiento promedio de cacao en baba'), {'fields' : (('cacao_baba','area_cacao_baba'),)}),
		(('Rendimiento promedio de cacao seco'), {'fields' : (('cacao_seco','area_cacao_seco'),)}),
	]

class InfraestructuraInline(admin.TabularInline):
	model = Infraestructura
	max_num = 10
	extra = 1
	can_delete = True

class Comercializacion_OrgInline(admin.TabularInline):
	model = Comercializacion_Org
	can_delete = False
	max_num = 1

class Comercializacion_ImportanciaInline(admin.TabularInline):
	model = Comercializacion_Importancia
	extra = 1
	can_delete = False

class Acopio_ComercioInline(admin.TabularInline):
	model = Acopio_Comercio
	max_num = 1
	can_delete = False

class OrganizacionAdmin(admin.ModelAdmin):
	# def get_queryset(self, request):
	# 	if request.user.is_superuser:
	# 		return Organizacion.objects.all()
	# 	return Organizacion.objects.filter(usuario=request.user)

	# def save_model(self, request, obj, form, change):
	# 	obj.usuario = request.user
	# 	obj.save()

	fieldsets = [
		(('Información de la Organización'), {'fields' : (('nombre','siglas'),('gerente',),('status','fundacion'),
			('direccion','municipio','telefono'),('fax','email'),('web','tipo')
			)}),
	]
	list_display = ('siglas','gerente','status','municipio')
	list_display_links = ('siglas',)
	list_filter = ('status',)
	search_fields = ['nombre','siglas']

class Encuesta_OrgAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		if request.user.is_superuser:
			return Encuesta_Org.objects.all()
		return Encuesta_Org.objects.filter(usuario=request.user)

	def save_model(self, request, obj, form, change):
		obj.usuario = request.user
		obj.save()

	exclude = ('usuario',)
	fieldsets = [
		('Información de la Organización', {'fields': ('fecha','organizacion')}),
	]

	inlines = [Aspectos_JuridicosInline,DocumentacionInline,Datos_ProductivosInline,InfraestructuraInline,
				Comercializacion_OrgInline,Comercializacion_ImportanciaInline,Acopio_ComercioInline]
	list_display = ('organizacion','fecha')
	# list_display_links = ('organizacion',)
	#list_filter = ('organizacion__municipio',)
	search_fields = ['organizacion__nombre','organizacion__siglas']

	class Media:
		js = ('js/admin_org.js',)
	
admin.site.register(Organizacion,OrganizacionAdmin)
admin.site.register(Status)
admin.site.register(Encuesta_Org,Encuesta_OrgAdmin)