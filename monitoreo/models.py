# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from lugar.models import *
from smart_selects.db_fields import ChainedForeignKey
from multiselectfield import MultiSelectField

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

class Situacion(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Situación"
		verbose_name_plural = "Situaciones"

class Lista_Certificaciones(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Certificación"
		verbose_name_plural = "Certificaciones"

class Actividades_Produccion(models.Model):
	nombre = models.CharField(max_length=200)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name = "Actividad de Producción"
		verbose_name_plural = "Actividades de Producción"

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
		
class Tenencia_Propiedad(models.Model):
	si = models.IntegerField(choices=PROPIEDAD_CHOICE,
		verbose_name='En el caso Si, a nombre de quien esta la propiedad',null=True,blank=True)
	no = models.ForeignKey(Situacion,verbose_name='En el caso que diga NO, especifique la situación',
		null=True,blank=True)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "2 Tenencia de Propiedad"
		verbose_name_plural = "2 Tenencia de Propiedad"

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
		verbose_name = "3 Uso de Tierra"
		verbose_name_plural = "3 Uso de Tierra"


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
		verbose_name = "4 Reforestación"
		verbose_name_plural = "4 Reforestación"

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
		verbose_name = "5 Caracterización de terreno"
		verbose_name_plural = "5 Caracterización de terreno"

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
		verbose_name = "6 Fenómenos naturales"
		verbose_name_plural = "6 Fenómenos naturales"

P_IMPRODUCTIVAS_CHOICES = (
	(1,'Alto (40%)'),
	(2,'Medio (30%)'),
	)

class Razones_Agricolas(models.Model):
	plantas_improductivas = models.IntegerField(choices=P_IMPRODUCTIVAS_CHOICES)
	plagas_enfermedades = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Plagas y enfermedades')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 Razones agrícolas"
		verbose_name_plural = "6 Razones agrícolas"

class Razones_Mercado(models.Model):
	bajo_precio = models.IntegerField(choices=SI_NO_CHOICES)
	falta_venta = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Falta de venta')
	estafa_contrato = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Estafa de contrato')
	calidad_producto = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Mala calidad de producto')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 Razones de mercado"
		verbose_name_plural = "6 Razones de mercado"

class Inversion(models.Model):
	invierte_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Invierte en cacao')
	interes_invertrir = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Interés de invertir')
	falta_credito = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Falta de crédito')
	altos_intereses = models.IntegerField(choices=SI_NO_CHOICES)
	robo_producto = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Robo de producto')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "6 Inversión"
		verbose_name_plural = "6 Inversión"

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
		verbose_name = "7 Mitigación de Riesgos"
		verbose_name_plural = "7 Mitigación de Riesgos"

class Organizacion_Asociada(models.Model):
	organizacion = models.ManyToManyField(Organizaciones,verbose_name='Organización/Institución con la que trabaja')
	tipos_servicio = models.ManyToManyField(Tipos_Servicio,verbose_name='Tipos de servicios que recibe')
	beneficios = models.ManyToManyField(Beneficios,verbose_name='Beneficios de estar asociado')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "8 Org. productiva-comercial asociado"
		verbose_name_plural = "8 Org. productiva-comercial asociado"

class Area_Cacao(models.Model):
	area = models.FloatField(verbose_name='Área total de cacao establecida en finca(Mz)')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "9 Área de cacao en finca"
		verbose_name_plural = "9 Área de cacao en fincas"

EDAD_PLANTA_CHOICES = (
	(1,'Menor de un año'),
	(2,'De 1 a 3 años'),
	(3,'De 4 a 10 años'),
	(4,'De 10 a 20 años'),
	(5,'Mayores de 20 años'),
	)

class Plantacion(models.Model):
	edad = models.IntegerField(choices=EDAD_PLANTA_CHOICES)
	area = models.FloatField(verbose_name='Área en Mz')
	edad_real = models.FloatField(verbose_name='Edad real de la Plantación (años)')
	numero_p_semilla = models.IntegerField(verbose_name='Número de plantas establecidas por semilla')
	numero_p_injerto = models.IntegerField(verbose_name='Número de plantas establecidas por injerto')
	numero_p_improductivas = models.IntegerField(verbose_name='Número de plantas improductivas en el área')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "9-1 Edad de la plantación"
		verbose_name_plural = "9-1 Edad de la plantación"


MESES_CHOICES = (
	(1,'Enero'),
	(2,'Febrero'),
	(3,'Marzo'),
	(4,'Abril'),
	(5,'Mayo'),
	(6,'Junio'),
	(7,'Julio'),
	(8,'Agosto'),
	(9,'Septiembre'),
	(10,'Octubre'),
	(11,'Noviembre'),
	(12,'Diciembre'),
	)

class Produccion_Cacao(models.Model):
	produccion_c_baba = models.FloatField(verbose_name='Producción cacao en baba (qq baba/seco)')
	produccion_c_seco = models.FloatField(verbose_name='Producción cacao seco sin fermentar (qq seco)')
	produccion_c_fermentado = models.FloatField(verbose_name='Producción cacao fermentado convencional (qq seco)')
	produccion_c_organico = models.FloatField(verbose_name='Producción cacao organico (qq seco)')
	meses_produccion = MultiSelectField(choices=MESES_CHOICES,verbose_name='Meses de mayor producción de cacao')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "9-2 Producción de cacao último año"
		verbose_name_plural = "9-2 Producción de cacao último año"

QUIEN_CERTIFICA_CHOICES = (
	(1,'UTZ/Sello'),
	(2,'FAIR TRADE'),
	(3,'SPP'),
	)

class Certificacion(models.Model):
	tipo = models.ManyToManyField(Lista_Certificaciones,verbose_name='Tipo de certificación')
	mant_area_cacao = models.FloatField(verbose_name='Mantenimiento de área de cacao (C$)')
	mant_area_finca = models.FloatField(verbose_name='Mantenimiento de la finca (C$)')
	quien_certifica = models.IntegerField(choices=QUIEN_CERTIFICA_CHOICES,verbose_name='¿Quién certifica?')
	paga_certificacion = models.ManyToManyField(Organizaciones,verbose_name='¿Quién paga la certificación?')
	costo_ccertificacion = models.FloatField(verbose_name='Costo de estar certificado')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "10-1 Tipo de certificación que posee"
		verbose_name_plural = "10-1 Tipo de certificación que posee"

VIVEROS_CHOICES = (
	(1,'Preparación del sitio'),
	(2,'Preparación del sustrato'),
	(3,'Llenado de bolsa'),
	(4,'Selección de semilla'),
	(5,'Siembra de semilla'),
	(6,'Uso de riego'),
	(7,'Control de malas hierba'),
	(8,'Fertilización orgánica'),
	)

FERTILIZACION_CHOICES = (
	(1,'Aplicación de té de estiércol'),
	(2,'Aplicación de gallinaza'),
	(3,'Aplicación de Bocashi'),
	(4,'Aplicación de foliares naturales'),
	(5,'Uso de triple cal'),
	(6,'Aplicación de lombrihumus'),
	(7,'Aplicación de urea'),
	(8,'Aplicación de fertilizante completo'),
	)

P_MANEJO_FIS_CHOICES = (
	(1,'Control de malas hierbas con machete'),
	(2,'Aplica herbicidas para controlar las malas hierbas'),
	(3,'Manejo de plagas con productos naturales'),
	(4,'Manejo de enfermedades con productos naturales'),
	(5,'Manejo de enfermedades con fungicidas'),
	(6,'Recolección e eliminación de frutos enfermos'),
	)

P_MANEJO_PROD_CHOICES = (
	(1,'Poda de formación'),
	(2,'Poda de mantenimiento'),
	(3,'Poda de rehabilitación o renovación'),
	(4,'Regulación en sombra'),
	)

P_MEJORA_PLANT_CHOICES = (
	(1,'Selección de árboles superiores'),
	(2,'Injertación en árboles adultos'),
	(3,'Renovación de área con plantas injertadas'),
	(4,'Enriquecimiento de áreas con plantas injertadas'),
	)

P_MANEJO_POST_C_CHOICES = (
	(1,'Selección y clasificación de mazorcas por variedad'),
	(2,'Selección de cacao en baba a fermentar'),
	(3,'Fermentación en sacos'),
	(4,'Fermentación en cajones'),
	(5,'Fermentación en cajillas'),
	(6,'Lo vende en baba a un centro de acopio'),
	(7,'Solo la saca de la mazorca y lo seca'),
	(8,'Lo saca de la mazorca, lo lava y luego lo seca'),
	)

class Tecnicas_Aplicadas(models.Model):
	viveros = MultiSelectField(choices=VIVEROS_CHOICES)
	fertilizacion = MultiSelectField(choices=FERTILIZACION_CHOICES,verbose_name='Prácticas de fertilización')
	pract_manejo_fis = MultiSelectField(choices=P_MANEJO_FIS_CHOICES,verbose_name='Prácticas de manejo fitosanitario')
	pract_manejo_prod = MultiSelectField(choices=P_MANEJO_PROD_CHOICES,verbose_name='Prácticas de manejo productivo')
	pract_mejora_plat = MultiSelectField(choices=P_MEJORA_PLANT_CHOICES,verbose_name='Prácticas de mejoramiento de la plantación')
	pract_manejo_post_c = MultiSelectField(choices=P_MANEJO_POST_C_CHOICES,verbose_name='Prácticas de manejo postcosecha y beneficiado')
	acopio_cacao = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Acopio de cacao en la comunidad/municipio')
	acopio_org = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='Organización que acopia cacao')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "11 Técn. aplicadas área de cacao"
		verbose_name_plural = "11 Técn. aplicadas área de cacao"

PRODUCTO_CHOICES = (
	(1,'Mazorca de cacao (unidad)'),
	(2,'Semilla para siembra (unidad)'),
	(3,'Cacao en baba (qq)'),
	(4,'Cacao rojo sin fermentar (qq)'),
	(5,'Cacao fermentado (lb)'),
	(6,'Chocolate artesanal (lb)'),
	(7,'Cacao en polvo (lb)'),
	(8,'Cacao procesado/ pinolillo (lb)'),
	(9,'Cajeta de cacao (lb)'),
	(10,'Pasta de cacao (lb)'),
	(11,'Vino de cacao (lt)'),
	)

QUIEN_VENDE_CHOICES = (
	(1,'Comunidad'),
	(2,'Intermediario'),
	(3,'Mercado'),
	(4,'Cooperativa'),
	)

class Comercializacion_Cacao(models.Model):
	producto = models.IntegerField(choices=PRODUCTO_CHOICES)
	auto_consumo = models.FloatField(verbose_name='Auto-consumo')
	venta =  models.FloatField()
	precio_venta = models.FloatField(verbose_name='Precio venta por unidad')
	quien_vende = models.IntegerField(choices=QUIEN_VENDE_CHOICES,verbose_name='¿A quién le vende?')
	donde_vende = models.ManyToManyField(Municipio,verbose_name='¿Dónde lo vende?')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "12 Comercialización de cacao"
		verbose_name_plural = "12 Comercialización de cacao"

class Distancia_Comercio_Cacao(models.Model):
	distancia = models.FloatField()
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "12.1 Distancia recorrida (Km)"
		verbose_name_plural = "12.1 Distancia recorrida (Km)"

CAPACITACIONES_CHOICES = (
	(1,'Regular en sombra'),
	(2,'Poda'),
	(3,'Manejo de plagas y enfermedades'),
	(4,'Elaboración de abonos orgánicos'),
	(5,'Elaboración de productos para control de plagas'),
	(6,'Establecimiento de vivero'),
	(7,'Injertación de cacao'),
	(8,'Selección de árboles élites para producción de semillas'),
	(9,'Manejo de post-cosecha (selección, cosecha, fermentado, secado)'),
	(10,'Manejo de calidad de cacao'),
	(11,'Certificación orgánica'),
	)

OPCIONES_CAPACITACIONES_CHOICES = (
	(1,'Jefe familia varón'),
	(2,'Jefa familia mujer'),
	(3,'Hijos'),
	(4,'Hijas'),
	)

class Capacitaciones_Tecnicas(models.Model):
	capacitaciones = models.IntegerField(choices=CAPACITACIONES_CHOICES)
	opciones = MultiSelectField(choices=OPCIONES_CAPACITACIONES_CHOICES)
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "13.1 Capacitación familia"
		verbose_name_plural = "13.1 Capacitación familia"

CAPACITACIONES_SOCIO_CHOICES = (
	(1,'Formación y fortalecimiento organizacional'),
	(2,'Contabilidad básica y administración'),
	(3,'Equidad de género'),
	(4,'Manejo de créditos'),
	(5,'Administración de pequeños negocios'),
	(6,'Gestión empresarial'),
	(7,'Cadena de valor de cacao'),
	(8,'Transformación de cacao'),
	)


class Capacitaciones_Socioeconomicas(models.Model):
	capacitaciones_socio = models.IntegerField(choices=CAPACITACIONES_SOCIO_CHOICES,verbose_name='Capacitaciones')
	opciones_socio = MultiSelectField(choices=OPCIONES_CAPACITACIONES_CHOICES,verbose_name='Opciones')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "13.2 Capacitaciones socioeconómico/org"
		verbose_name_plural = "13.2 Capacitaciones socioeconómico/org"

PRIORIDAD_CHOICES = (
	(1,'1'),
	(2,'2'),
	(3,'3'),
	(4,'4'),
	(5,'5'),
	)

class Problemas_Cacao(models.Model):
	fertilidad = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Baja fertilidad del suelo')
	arboles = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Árboles poco productivos')
	plantaciones = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Plantaciones muy viejas')
	plagas = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Plagas y enfermedades')
	produccion = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Poca producción')
	mano_obra = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Poca disponibilidad de mano de obra')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "13.3 Problemas área de cacao"
		verbose_name_plural = "13.3 Problemas área de cacao"

DECISIONES_CHOICES = (
	(1,'Decide Usted sobre la siembra de cacao'),
	(2,'Decide Usted sobre la cosecha de cacao'),
	(3,'Decide Usted sobre la venta de cacao'),
	(4,'Decide Usted sobre la Ingresos de cacao'),
	)

class Genero(models.Model):
	actividades = models.ManyToManyField(Actividades_Produccion,verbose_name='Actividades en las que participa')
	ingresos = models.IntegerField(choices=SI_NO_CHOICES,verbose_name='¿Usted recibe ingresos por las actividades que realiza?')
	ingreso_mesual = models.FloatField(null=True,blank=True,verbose_name='Ingreso mensual aproximado percibido')
	destino_ingresos = models.CharField(max_length=300,verbose_name='Destino de los ingresos percibidos')
	decisiones = MultiSelectField(choices=DECISIONES_CHOICES,verbose_name='Decisiones sobre destino de la producción')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "14 Género"
		verbose_name_plural = "14 Género"

class Genero_2(models.Model):
	ganaderia = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Ganadería')
	granos_basicos = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Granos Básicos')
	cacao = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Cacao')
	cafe = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Café')
	madera = models.IntegerField(choices=PRIORIDAD_CHOICES,verbose_name='Madera')
	encuesta = models.ForeignKey(Encuesta)

	class Meta:
		verbose_name = "Sobre otros Ingresos"
		verbose_name_plural = "Sobre otros Ingresos"