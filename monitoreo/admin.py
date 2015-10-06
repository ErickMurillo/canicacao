# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.flatpages.models import FlatPage
# Note: we are renaming the original Admin and Form as we import them!
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.forms import FlatpageForm as FlatpageFormOld

from ckeditor.widgets import CKEditorWidget
 
class FlatpageForm(FlatpageFormOld):
	content = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = FlatPage # this is not automatically inherited from FlatpageFormOld
		fields = '__all__'
 
class FlatPageAdmin(FlatPageAdminOld):
	form = FlatpageForm

class Familia_Inline(admin.TabularInline):
	model = Familia
	max_num = 1
	can_delete = False

class Educacion_Inline(admin.TabularInline):
	model = Educacion
	extra = 1
	max_num = 9
	can_delete = True
	form = EducacionForm

class Tenencia_Propiedad_Inline(admin.TabularInline):
	model = Tenencia_Propiedad
	max_num = 1
	can_delete = False

class Uso_Tierra_Inline(admin.StackedInline):
	model = Uso_Tierra
	max_num = 1
	can_delete = False
	fieldsets = [
		('Área total en manzanas que tiene la propiedad',{'fields': ['area_total']}),
		('Número de manzanas en la que esta distribuida la finca', {'fields': [('bosque','tacotal','cultivo_anual'),
																				('plantacion_forestal','area_pasto_abierto','area_pasto_arboles'),
																				('cultivo_perenne','cultivo_semi_perenne','cacao'),
																				('huerto_mixto_cacao','cafe','otros')
			]}),
	]
	form = Uso_TierraForm

class Reforestacion_Inline(admin.TabularInline):
	model = Reforestacion
	max_num = 1
	can_delete = False

class Caracterizacion_Terreno_Inline(admin.TabularInline):
	model = Caracterizacion_Terreno
	max_num = 1
	can_delete = False

class Fenomenos_Naturales_Inline(admin.TabularInline):
	model = Fenomenos_Naturales
	max_num = 1
	can_delete = False

class Razones_Agricolas_Inline(admin.TabularInline):
	model = Razones_Agricolas
	max_num = 1
	can_delete = False

class Razones_Mercado_Inline(admin.TabularInline):
	model = Razones_Mercado
	max_num = 1
	can_delete = False

class Inversion_Inline(admin.TabularInline):
	model = Inversion
	max_num = 1
	can_delete = False

class Mitigacion_Riesgos_Inline(admin.TabularInline):
	model = Mitigacion_Riesgos
	max_num = 1
	can_delete = False

class Organizacion_Asociada_Inline(admin.TabularInline):
	model = Organizacion_Asociada
	max_num = 1
	can_delete = False

class Area_Cacao_Inline(admin.TabularInline):
	model = Area_Cacao
	max_num = 1
	can_delete = False

class Plantacion_Inline(admin.TabularInline):
	model = Plantacion
	max_num = 5
	extra = 1
	can_delete = False

class Produccion_Cacao_Inline(admin.TabularInline):
	model = Produccion_Cacao
	max_num = 1
	can_delete = False

class Certificacion_Inline(admin.StackedInline):
	model = Certificacion
	max_num = 1
	can_delete = False
	fieldsets = (
		(None, {
			'fields': (('cacao_certificado', 'tipo', 'quien_certifica', 'paga_certificacion','costo_certificacion'),)
		}),
		('Costo de producción', {
			'fields': ('mant_area_cacao', 'mant_area_finca')
		}),
	)

class Tecnicas_Aplicadas_Inline(admin.StackedInline):
	model = Tecnicas_Aplicadas
	max_num = 1
	can_delete = False

class Comercializacion_Cacao_Inline(admin.TabularInline):
	model = Comercializacion_Cacao
	max_num = 11
	extra = 1
	can_delete = False

class Distancia_Comercio_Cacao_Inline(admin.TabularInline):
	model = Distancia_Comercio_Cacao
	max_num = 1
	can_delete = False

class Capacitaciones_Tecnicas_Inline(admin.TabularInline):
	model = Capacitaciones_Tecnicas
	max_num = 11
	extra = 1
	can_delete = False

class Capacitaciones_Socioeconomicas_Inline(admin.TabularInline):
	model = Capacitaciones_Socioeconomicas
	max_num = 8
	extra = 1
	can_delete = False

class Problemas_Cacao_Inline(admin.TabularInline):
	model = Problemas_Cacao
	max_num = 1
	can_delete = False

class Genero_Inline(admin.StackedInline):
	model = Genero
	max_num = 1
	can_delete = False
	fieldsets = [(None, {'fields' : (('actividades'),('ingresos','ingreso_mesual'),('destino_ingresos_2',),('decisiones',))}),
	]

class Genero_2_Inline(admin.TabularInline):
	model = Genero_2
	max_num = 1
	can_delete = False

class Adicional_Inline(admin.TabularInline):
	model = Adicional
	max_num = 1
	can_delete = False

class EncuestaAdmin(admin.ModelAdmin):
	def get_queryset(self, request):
		if request.user.is_superuser:
			return Encuesta.objects.all()
		return Encuesta.objects.filter(usuario=request.user)

	def save_model(self, request, obj, form, change):
		if not request.user.is_superuser:
			obj.usuario = request.user
			obj.save()

	def get_form(self, request, obj=None, **kwargs):
		if request.user.is_superuser:
			self.exclude = ('anno',)
			self.fieldsets = [(('Informacion Básica'), {'fields' : (('fecha',),('organizacion','recolector'),('persona','usuario'))}),]
		else:
			self.exclude = ('usuario','anno')
			self.fieldsets = [(('Informacion Básica'), {'fields' : (('fecha',),('organizacion','recolector'),('persona',))}),]
		return super(EncuestaAdmin, self).get_form(request, obj=None, **kwargs)

	def get_list_filter(self, request):
		if request.user.is_superuser:
			return ('organizacion',)
		else:
			return ()

	list_display = ('persona','organizacion','recolector')
	list_display_links = ('organizacion','persona')
	search_fields = ['persona__nombre','recolector__nombre']

	inlines = [Familia_Inline,Educacion_Inline,Tenencia_Propiedad_Inline,Uso_Tierra_Inline,Reforestacion_Inline,
				Caracterizacion_Terreno_Inline,Fenomenos_Naturales_Inline,Razones_Agricolas_Inline,Razones_Mercado_Inline,
				Inversion_Inline,Mitigacion_Riesgos_Inline,Organizacion_Asociada_Inline,Area_Cacao_Inline,Plantacion_Inline,
				Produccion_Cacao_Inline,Certificacion_Inline,Tecnicas_Aplicadas_Inline,Comercializacion_Cacao_Inline,
				Distancia_Comercio_Cacao_Inline,Capacitaciones_Tecnicas_Inline,Capacitaciones_Socioeconomicas_Inline,
				Problemas_Cacao_Inline,Genero_Inline,Genero_2_Inline,Adicional_Inline
				]

	class Media:
		js = ('js/admin.js',)
		css = {
			'all': ('css/admin.css',)
		}
	  
admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(Recolector)
admin.site.register(Situacion)
admin.site.register(Tipos_Servicio)
admin.site.register(Beneficios)
admin.site.register(Lista_Certificaciones)
admin.site.register(Actividades_Produccion)
admin.site.register(Persona)
admin.site.register(Quien_Certifica)
admin.site.register(Paga_Certifica)
admin.site.register(Profesion)
admin.site.register(Destino_Ingresos)
admin.site.register(Tecnologias)
# We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
