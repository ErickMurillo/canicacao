# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from lugar.models import *
from multiselectfield import MultiSelectField

# Create your models here.
class Status(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Status Legal"
		verbose_name_plural = "Status Legal"

TIPO_CHOICES = (
	(1,'Miembro Canicacao'),
	(1,'Organización de apoyo'),
	)
class Organizacion(models.Model):
	nombre = models.CharField(max_length=200,verbose_name='Organización/Institución')
	siglas = models.CharField(max_length=200)
	gerente = models.CharField(max_length=200,verbose_name='Representante legal',null=True,blank=True)
	status = models.ForeignKey(Status,verbose_name='Status Legal',null=True,blank=True)
	fundacion = models.DateField(verbose_name='Año fundación',null=True,blank=True)
	direccion = models.CharField(max_length=300,null=True,blank=True)
	municipio = models.ForeignKey(Municipio)
	telefono = models.IntegerField(verbose_name='Número telefónico',null=True,blank=True)
	fax = models.IntegerField(verbose_name='Número fax',null=True,blank=True)
	email = models.EmailField(null=True,blank=True)
	web = models.URLField(verbose_name='Página web',null=True,blank=True)
	tipo = models.IntegerField(choices=TIPO_CHOICES,verbose_name='Tipo de Organización',null=True,blank=True)
	#usuario = models.ForeignKey(User)

	def __unicode__(self):
		return self.siglas

	def save(self, *args, **kwargs):
		if not  self.id:
			self.slug = slugify(self.siglas)
		super(Organizacion, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Organización"
		verbose_name_plural = "Organizaciones"
		unique_together = ("nombre",)

SI_NO_CHOICES = (
	(1,'Si'),
	(2,'No'),
	)

class Encuesta_Org(models.Model):
	fecha = models.DateField()
	organizacion = models.ForeignKey(Organizacion,related_name='Organizacion')
	anno = models.IntegerField()
	usuario = models.ForeignKey(User,related_name='User')

	def __unicode__(self):
		return self.organizacion.siglas

	def save(self, *args, **kwargs):
		self.anno = self.fecha.year 
		super(Encuesta_Org, self).save(*args, **kwargs)

	class Meta:
		verbose_name = "Encuesta"
		verbose_name_plural = "Encuestas"

class Aspectos_Juridicos(models.Model):
	tiene_p_juridica = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Personería jurídica')
	act_p_juridica = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Actualización personería jurídica')
	solvencia_tributaria = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Cuenta con solvencia tributaria (DGI)')
	junta_directiva = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Junta Directiva certificada')
	mujeres = models.IntegerField(verbose_name='Miembros mujeres JD')
	hombres = models.IntegerField(verbose_name='Miembros hombres JD')
	lista_socios = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Lista socias/os esta actualizada y certificada')
	ruc = models.CharField(max_length=50,verbose_name='No. RUC',null=True,blank=True)
	#organizacion = models.ForeignKey(Organizacion)
	encuesta = models.ForeignKey(Encuesta_Org,null=True,blank=True)

	class Meta:
		verbose_name = "Aspectos jurídicos"
		verbose_name_plural = "Aspectos jurídicos"

DOCUMENTOS_CHOICES = (
	(1,'Poseen estatutos'),
	(2,'Cuentan con plan estratégico'),
	(3,'Poseen libro de Actas'),
	(4,'Tiene plan de negocios'),
	(5,'Cuentan con plan de acopio'),
	(6,'Poseen plan de comercialización'),
	)

class Documentacion(models.Model):
	documentos = models.IntegerField(choices=DOCUMENTOS_CHOICES)
	si_no = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Si/No')
	fecha = models.DateField(verbose_name='Fecha de elaboración u actualización')
	#organizacion = models.ForeignKey(Organizacion)
	encuesta = models.ForeignKey(Encuesta_Org,null=True,blank=True)

	class Meta:
		verbose_name = "Inform. sobre documentación en gestión"
		verbose_name_plural = "Inform. sobre documentación en gestión"

class Datos_Productivos(models.Model):
	socias = models.IntegerField()
	socios = models.IntegerField()
	pre_socias = models.IntegerField()
	pre_socios = models.IntegerField()
	area_total = models.FloatField(verbose_name='Área total establecida por sus socias/os')
	area_cert_organico = models.FloatField(verbose_name='Área con certificado orgánico')
	area_convencional = models.FloatField(verbose_name='Área convencional')
	cacao_baba = models.FloatField(verbose_name='QQ')
	area_cacao_baba =models.FloatField(verbose_name='Mz')
	cacao_seco = models.FloatField(verbose_name='QQ')
	area_cacao_seco =models.FloatField(verbose_name='Mz')
	#organizacion = models.ForeignKey(Organizacion)
	encuesta = models.ForeignKey(Encuesta_Org,null=True,blank=True)

	class Meta:
		verbose_name = "Datos productivos de la Org. y asociado"
		verbose_name_plural = "Datos productivos de la Org. y asociado"

INFRAESTRUCTURA_CHOICES = (
	(1,'Centro de Acopio central'),
	(2,'Centro de acopio comunitarios'),
	(3,'Hornos de secado'),
	(4,'Planta de procesamiento'),
	(5,'Bodegas'),
	(6,'Cuartos fríos'),
	(7,'Oficina'),
	(8,'Medios de Transporte'),
	)

ESTADO_CHOICES = (
	(1,'Bueno'),
	(2,'Malo'),
	(3,'Regular'),
	)

class Infraestructura(models.Model):
	tipo = models.IntegerField(choices=INFRAESTRUCTURA_CHOICES,verbose_name='Tipo de Infraestructura')
	cantidad = models.FloatField()
	capacidad = models.FloatField(verbose_name='Capacidad de las instalaciones (qq)')
	anno_construccion = models.DateField(verbose_name='Año de construcción')
	estado = models.IntegerField(choices=ESTADO_CHOICES,verbose_name='Estado de infraestructura')
	#organizacion = models.ForeignKey(Organizacion)
	encuesta = models.ForeignKey(Encuesta_Org,null=True,blank=True)

	class Meta:
		verbose_name = "Infraestructura y maquinaria"
		verbose_name_plural = "Infraestructura y maquinaria"

TIPO_PROD_CHOICES = (
	(1,'Caco rojo'),
	(2,'Cacao fermentado'),
	(3,'Ambos'),
	)

TIPO_MERCADO_CHOICES = (
	(1,'Convencional'),
	(2,'Orgánico'),
	(3,'Comercio Justo'),
	(4,'UTZ'),
	)

DESTINO_CHOICES = (
	(1,'Mercado Local'),
	(2,'Mercado Nacional'),
	(3,'Mercado Internacional'),
	)

class Comercializacion_Org(models.Model):
	#fecha = models.IntegerField(verbose_name='Año de recolección de información')
	cacao_baba_acopiado = models.FloatField(verbose_name='Cacao en baba acopiado (qq)')
	cacao_seco_comercializado = models.FloatField(verbose_name='Cacao en seco comercializado (qq)')
	socios_cacao = models.IntegerField(verbose_name='Socios que entregaron cacao al acopio')
	productores_no_asociados = models.IntegerField(verbose_name='Productores no asociados')
	tipo_producto = models.IntegerField(choices=TIPO_PROD_CHOICES,verbose_name='Tipo de producto comercializado')
	tipo_mercado = MultiSelectField(choices=TIPO_MERCADO_CHOICES)
	destino_produccion = MultiSelectField(choices=DESTINO_CHOICES)
	#organizacion = models.ForeignKey(Organizacion)
	encuesta = models.ForeignKey(Encuesta_Org,null=True,blank=True)

	class Meta:
		verbose_name = "Comercialización de la Organización"
		verbose_name_plural = "Comercialización de la Organización"

class Comercializacion_Importancia(models.Model):
	orden_importancia = models.CharField(max_length=200,verbose_name='Donde comercializa su cacao (por orden de importancia)')
	#organizacion = models.ForeignKey(Organizacion)
	encuesta = models.ForeignKey(Encuesta_Org,null=True,blank=True)

	class Meta:
		verbose_name = "Comercialización Cacao"
		verbose_name_plural = "Comercialización Cacao"

ACOPIO_COMERCIO_CHOICES = (
	(1,'Propio'),
	(2,'Crédito bancario'),
	(3,'Cooperación Internacional'),
	(4,'Financiamiento del comprador'),
	)

class Acopio_Comercio(models.Model):
	seleccion = MultiSelectField(choices=ACOPIO_COMERCIO_CHOICES)
	#organizacion = models.ForeignKey(Organizacion)
	encuesta = models.ForeignKey(Encuesta_Org,null=True,blank=True)

	class Meta:
		verbose_name = "Financiamiento de acopio y comerc."
		verbose_name_plural = "Financiamiento de acopio y comerc."