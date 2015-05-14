# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
class Organizaciones(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Organización"
		verbose_name_plural = "Organizaciones"


class Recolector(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Recolector"
		verbose_name_plural = "Recolectores"

class Tipos_Servicio(models.Model):
	servicio = models.CharField(max_length=200)

	def __unicode__(self):
		return self.servicio

	class Meta:
		verbose_name = "Tipo de Servicio"
		verbose_name_plural = "Tipos de Servicios"

class Beneficios(models.Model):
	beneficio = models.CharField(max_length=200)

	def __unicode__(self):
		return self.beneficio

	class Meta:
		verbose_name = "Beneficio"
		verbose_name_plural = "Beneficios"

SEXO_CHOICE = (
	(1,'Hombre'),
	(2,'Mujer')
	)

PROFESION_CHOICE = (
	(1,'Agricultor'),
	(2,'-----')
	)
class Encuesta(models.Model):
	fecha = models.DateField()
	recolector = models.ForeignKey(Recolector)
	organizacion = models.ForeignKey(Organizaciones,verbose_name='Organización')
	nombre =  models.CharField(max_length=200,verbose_name='Nombre de jefa/e de familia')
	cedula = models.CharField(max_length=20,verbose_name='Céula de entrevistado/a',null=True,blank=True)
	fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento')
	sexo = models.IntegerField(choices=SEXO_CHOICE)
	profesion = models.IntegerField(choices=PROFESION_CHOICE)
	nombre_finca = models.CharField(max_length=200,verbose_name='Nombre de la Finca')
	departamento = models.ForeignKey(Departamento)
	municipio = ChainedForeignKey(
                                Municipio,
                                chained_field="departamento", 
                                chained_model_field="departamento",
                                show_all=False, auto_choose=True)
	comunidad = ChainedForeignKey(
                                Comunidad,
                                chained_field="municipio", 
                                chained_model_field="municipio",
                                show_all=False, auto_choose=True)
	latitud = models.FloatField(null=True,blank=True)
	longitud = models.FloatField(null=True,blank=True)
	usuario = models.ForeignKey(User)


	def __unicode__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		if not  self.id:
			self.slug = slugify(self.nombre)
		super(Encuesta, self).save(*args, **kwargs)

class Familia(models.Model):
	miembros = models.IntegerField(verbose_name='Número de miembros')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "1-1 Miembros de la Familia"
		verbose_name_plural = "1-1 Miembros de la Familia"

RANGOS_CHOICE = (
		(1,'Hombres mayores 31 años'),
		(2,'Mujeres mayores 31 años'),
		(3,'Hombre joven 19 a 30 años'),
		(4,'Mujer joven 19 a 30 años'),
		(5,'Hombre adoles. 13 a 18 años'),
		(6,'Mujer adoles. 13 a 18 años'),
		(7,'Niños 0 a 12 años'),
		(8,'Niñas 0 a 12 años'),
		(9,'Ancianos (> 64 años)'),
		)

class Educacion(models.Model):
	rango = models.IntegerField(choices=RANGOS_CHOICE,verbose_name='Selección')
	numero_total = models.IntegerField()
	no_lee_ni_escribe = models.IntegerField()
	primaria_incompleta = models.IntegerField()
	primaria_completa = models.IntegerField()
	secundaria_incompleta = models.IntegerField()
	bachiller = models.IntegerField()
	universitario_tecnico = models.IntegerField()
	viven_fuera = models.IntegerField(verbose_name='Número de personas que viven fuera de la finca')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "1-2 Nivel de educación de la Familia"
		verbose_name_plural = "1-2 Nivel de educación de la Familia"

PROPIEDAD_CHOICE = (
	(1,'A nombre del Hombre'),
	(2,'A nombre de la Mujer'),
	(3,'A nombre de Hijas/hijos'),
	(4,'A nombre del Hombre y Mujer'),
	)
class Situacion(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre
		
class Tenencia_Propiedad(models.Model):
	si = models.IntegerField(choices=PROPIEDAD_CHOICE,
		verbose_name='En el caso Si, a nombre de quien esta la propiedad',null=True,blank=True)
	no = models.ForeignKey(Situacion,verbose_name='En el caso que diga NO, especifique la situación',
		null=True,blank=True)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "2 - Tenencia de Propiedad"
		verbose_name_plural = "2 - Tenencia de Propiedad"

class Uso_Tierra(models.Model):
	area_total = models.FloatField(verbose_name='Área total en manzanas de la propiedad')
	bosque = models.FloatField(verbose_name='Bosques')
	tacotal = models.FloatField(verbose_name='Tacotal o área de descanso')
	cultivo_anual = models.FloatField(verbose_name='Cultivo anual ( que produce en el año)')
	plantacion_forestal = models.FloatField(verbose_name='Plantación forestal ( madera y leña)')
	area_pasto_abierto = models.FloatField(verbose_name='Área de pastos abierto')
	area_pasto_arboles = models.FloatField(verbose_name='Área de pastos con árboles')
	cultivo_perenne = models.FloatField(verbose_name='Cultivo perenne (frutales)')
	cultivo_semi_perenne = models.FloatField(verbose_name='Cultivo semi-perenne (musácea, piña)')
	cacao = models.FloatField(verbose_name='Solo destinado para cacao')
	huerto_mixto_cacao = models.FloatField(verbose_name='Huerto mixto con cacao')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "3 - Uso de Tierra"
		verbose_name_plural = "3 - Uso de Tierra"

SI_NO_CHOICES = (
	(1,'Si'),
	(2,'No')
	)

class Reforestacion(models.Model):
	enriquecimiento_bosques = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Enriquecimiento de los bosques')
	proteccion_agua = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Protección de fuentes de agua')
	cercas_vivas = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Establecimiento de cercas viva')
	viveros = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Establecimiento de viveros')
	siembre_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Siembra de árboles en cacao')
	forestales = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Plantaciones forestales')
	potrero = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Siembra de árboles en potrero')
	frutales = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Parcelas frutales')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "4 - Reforestación"
		verbose_name_plural = "4 - Reforestación"

TEXTURA_CHOICES = (
	(1,'Arcilloso'),
	(2,'Limoso'),
	(3,'Arenoso'),
	(4,'Franco'),
	(5,'Franco arenoso'),
	)
PENDIENTE_CHOICES = (
	(1,'Plana'),
	(2,'Inclinada'),
	(3,'Muy inclinada'),
	)

HOJARASCA_CHOICES = (
	(1,'Alta'),
	(2,'Medio'),
	(3,'Baja'),
	)

PROFUNDIDAD_CHOICES = (
	(1,'Poco profundo'),
	(2,'Medio profundo'),
	(3,'Muy profundo'),
	)

DRENAJE_CHOICES = (
	(1,'Bueno'),
	(2,'Regular'),
	(3,'Malo'),
	)

class Caracterizacion_Terreno(models.Model):
	textura_suelo = models.IntegerField(choices=TEXTURA_CHOICES,verbose_name='¿Cuál es el tipo de textura del suelo?')
	pendiente_terreno = models.IntegerField(choices=PENDIENTE_CHOICES,verbose_name='¿Cuál es la pendiente del terreno?')
	contenido_hojarasca = models.IntegerField(choices=HOJARASCA_CHOICES,verbose_name='¿Cómo en el contenido de hojarasca?')
	porfundidad_suelo = models.IntegerField(choices=PROFUNDIDAD_CHOICES,verbose_name='¿Cuál es la profundidad de suelo?')
	drenaje_suelo = models.IntegerField(choices=DRENAJE_CHOICES,verbose_name='¿Cómo en el drenaje del suelo?')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "5 - Caracterización de terreno"
		verbose_name_plural = "5 - Caracterización de terreno"

RIESGOS_CHOICES = (
	(1,'Fuerte'),
	(2,'Poco fuerte'),
	(3,'Leve'),
	)

class Fenomenos_Naturales(models.Model):
	sequia = models.IntegerField(choices=RIESGOS_CHOICES,verbose_name='Sequía')
	innundacion = models.IntegerField(choices=RIESGOS_CHOICES,verbose_name='Inundación')
	lluvia = models.IntegerField(choices=RIESGOS_CHOICES)
	viento = models.IntegerField(choices=RIESGOS_CHOICES)
	deslizamiento = models.IntegerField(choices=RIESGOS_CHOICES)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 - Fenómenos naturales"
		verbose_name_plural = "6 - Fenómenos naturales"

P_IMPRODUCTIVAS_CHOICES = (
	(1,'Alto (40%)'),
	(2,'Medio (30%)'),
	)

class Razones_Agricolas(models.Model):
	plantas_improductivas = models.IntegerField(choices=P_IMPRODUCTIVAS_CHOICES)
	plagas_enfermedades = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Plagas y enfermedades')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 - Razones agrícolas"
		verbose_name_plural = "6 - Razones agrícolas"

class Razones_Mercado(models.Model):
	bajo_precio = models.IntegerField(choices=SI_NO_CHOICES)
	falta_venta = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Falta de venta')
	estafa_contrato = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Estafa de contrato')
	calidad_producto = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Mala calidad de producto')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 - Razones de mercado"
		verbose_name_plural = "6 - Razones de mercado"

class Inversion(models.Model):
	invierte_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Invierte en cacao')
	interes_invertrir = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Interés de invertir')
	falta_credito = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Falta de crédito')
	altos_intereses = models.IntegerField(choices=SI_NO_CHOICES)
	robo_producto = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Robo de producto')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 - Inversión"
		verbose_name_plural = "6 - Inversión"

class Mitigacion_Riesgos(models.Model):
	monitoreo_plagas = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Realiza monitoreo de plagas y enfermedades?')
	manejo_cultivo = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Cuenta con un manejo adecuado para el cultivo?')
	manejo_recursos = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Disponen suficiente recursos para manejo de finca?')
	almacenamiento_agua = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Cuenta con obras para almacenamiento de agua?')
	distribucion_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Participan en cadena de distribución de producto cacao?')
	venta_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Cuenta con un contrato para la venta de cacao?')
	tecnologia_secado = models.CharField(max_length=200,null=True,blank=True,verbose_name='¿Dispone de tecnología para el secado y almacenamiento de cosecha? Mencione')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "7 - Mitigación de Riesgos"
		verbose_name_plural = "7 - Mitigación de Riesgos"

class Organizacion_Asociada(models.Model):
	organizacion = models.ManyToManyField(Organizaciones,verbose_name='Organización/Institución con la que trabaja')
	tipos_servicio = models.ManyToManyField(Tipos_Servicio,verbose_name='Tipos de servicios que recibe')
	beneficios = models.ManyToManyField(Beneficios,verbose_name='Beneficios de estar asociado')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "8 - Con que Organización productiva-comercial esta asociado"
		verbose_name_plural = "8 - Con que Organización productiva-comercial esta asociado"

class Area_Cacao(models.Model):
	area = models.FloatField(verbose_name='Área total de cacao establecida en finca(Mz)')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "9 - Área de cacao en finca"
		verbose_name_plural = "9 - Área de cacao en fincas"