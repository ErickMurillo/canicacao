# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

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
																				('huerto_mixto_cacao','otros')
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

class Certificacion_Inline(admin.TabularInline):
	model = Certificacion
	max_num = 1
	can_delete = False

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
	fieldsets = [(None, {'fields' : (('actividades'),('ingresos','ingreso_mesual','destino_ingresos'),('decisiones',))}),
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
		obj.usuario = request.user
		obj.save()

	exclude = ('usuario','anno')
	fieldsets = [
		(('Informacion Básica'), {'fields' : (('fecha',),('organizacion','recolector'),('persona',))}),
	]
	inlines = [Familia_Inline,Educacion_Inline,Tenencia_Propiedad_Inline,Uso_Tierra_Inline,Reforestacion_Inline,
				Caracterizacion_Terreno_Inline,Fenomenos_Naturales_Inline,Razones_Agricolas_Inline,Razones_Mercado_Inline,
				Inversion_Inline,Mitigacion_Riesgos_Inline,Organizacion_Asociada_Inline,Area_Cacao_Inline,Plantacion_Inline,
				Produccion_Cacao_Inline,Certificacion_Inline,Tecnicas_Aplicadas_Inline,Comercializacion_Cacao_Inline,
				Distancia_Comercio_Cacao_Inline,Capacitaciones_Tecnicas_Inline,Capacitaciones_Socioeconomicas_Inline,
				Problemas_Cacao_Inline,Genero_Inline,Genero_2_Inline,Adicional_Inline
				]

	list_display = ('persona','organizacion','recolector')
	list_display_links = ('organizacion','persona')
	list_filter = ('organizacion__siglas','recolector__nombre')
	search_fields = ['persona__nombre']
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
