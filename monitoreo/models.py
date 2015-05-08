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

class Recolector(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

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



