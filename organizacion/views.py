# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import *
import json as simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Sum, Count, Avg
import collections
from django.contrib.auth.decorators import login_required

# Create your views here.
def _queryset_filtrado(request):
	params = {}

	if request.session['departamento']:
		if not request.session['municipio']:
			municipios = Municipio.objects.filter(departamento__in=request.session['departamento'])
			params['organizacion__municipio__in'] = municipios
		else:
			params['organizacion__municipio__in'] = request.session['municipio']

	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	return Encuesta_Org.objects.filter(**params)

@login_required
def get_organizacion(request,template="organizacion/organizacion.html"):
	if request.method == 'POST':
		mensaje = None
		form = OrganizacionConsulta(request.POST)
		if form.is_valid():
			request.session['departamento'] = form.cleaned_data['departamento']
			request.session['municipio'] = form.cleaned_data['municipio']
			request.session['comunidad'] = form.cleaned_data['comunidad']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1

			return HttpResponseRedirect('/org-dashboard/')
		else:
			centinela = 0

	else:
		form = OrganizacionConsulta()
		mensaje = "Existen alguno errores"
		centinela = 0
		try:
			del request.session['departamento']
			del request.session['municipio']
			del request.session['comunidad']
		except:
			pass

	return render(request, template, locals())

@login_required
def get_org_detail(request,id=None,template="organizacion/orgdetail.html"):
	org = Organizacion.objects.get(id=id)

	anio = collections.OrderedDict()

	anios_list = Encuesta_Org.objects.filter(organizacion__id=id).order_by('anno').values_list('anno', flat=True).distinct('anno')

	for year in anios_list:
		aspectos_juridicos = {}
		for obj in Aspectos_Juridicos.objects.filter(encuesta__anno=year,encuesta__organizacion__id=id):
			aspectos_juridicos[year] = (obj.get_tiene_p_juridica_display(),obj.get_act_p_juridica_display(),
										obj.get_solvencia_tributaria_display(),obj.get_junta_directiva_display(),
										obj.hombres,obj.mujeres,obj.get_lista_socios_display(),obj.ruc)

		documentacion = []
		for obj in Documentacion.objects.filter(encuesta__anno=year,encuesta__organizacion__id=id):
			documentacion.append((obj.get_documentos_display(),obj.get_si_no_display(),obj.fecha))

		datos_productivos = {}
		for obj in Datos_Productivos.objects.filter(encuesta__anno=year,encuesta__organizacion__id=id):
			datos_productivos[year] = (obj.socias,obj.socios,obj.pre_socias,obj.pre_socios,obj.area_total,
										obj.area_cert_organico,obj.area_convencional,obj.cacao_baba,
										obj.area_cacao_baba,obj.cacao_seco,obj.area_cacao_seco)
		
		infraestructura = []
		for obj in Infraestructura.objects.filter(encuesta__anno=year,encuesta__organizacion__id=id):
			infraestructura.append((obj.get_tipo_display(),obj.cantidad,obj.capacidad,
									obj.anno_construccion,obj.get_estado_display()))
		 
		
		comercializacion_org = {}
		lista = []
		tipo_producto = {}
		for obj in Comercializacion_Org.objects.filter(encuesta__anno=year,encuesta__organizacion__id=id):
			comercializacion_org[year] = (obj.cacao_baba_acopiado,obj.cacao_seco_comercializado,
											obj.socios_cacao,obj.productores_no_asociados,
											obj.get_tipo_producto_display(),obj.tipo_mercado,
											obj.destino_produccion)

		comercializacion_importancia = []
		for obj in Comercializacion_Importancia.objects.filter(encuesta__anno=year,encuesta__organizacion__id=id):
			comercializacion_importancia.append(obj.orden_importancia)

		acopio_comercio = []
		for obj in Acopio_Comercio.objects.filter(encuesta__anno=year,encuesta__organizacion__id=id):
			acopio_comercio.append(obj.seleccion)

		anio[year] = (aspectos_juridicos,documentacion,datos_productivos,infraestructura,
						comercializacion_org,comercializacion_importancia,acopio_comercio)


	return render(request,template,locals())

def obtener_lista_org(request):
	if request.is_ajax():
		lista = []
		for objeto in Encuesta_Org.objects.all().distinct('organizacion'):
			dicc = dict(nombre=objeto.organizacion.municipio.nombre, id=objeto.organizacion.id,
						lon=float(objeto.organizacion.municipio.longitud),
						lat=float(objeto.organizacion.municipio.latitud)
						)
			lista.append(dicc)

		serializado = simplejson.dumps(lista)
		return HttpResponse(serializado, content_type='application/json')

@login_required
def status(request,template='organizacion/status.html'):
	filtro = _queryset_filtrado(request)

	organizaciones = filtro.distinct('organizacion__nombre').count()
	anno = collections.OrderedDict()

	anios_list = filtro.order_by('anno').values_list('anno', flat=True).distinct('anno')

	for year in anios_list:
		#status legal de las organizaciones -----------------------------------------
		status = {}
		for obj in Status.objects.all():
			conteo = filtro.filter(organizacion__status=obj,anno=year).count()
			status[obj] = conteo

		#aspectos juridicos ---------------------------------------------------------
		aspectos_juridicos = {}
		tabla_aspectos_juridicos = {}
		count_org = filtro.filter(anno=year).distinct('organizacion__nombre').count()
		for obj in SI_NO_CHOICES:
			personeria_juridica = filtro.filter(aspectos_juridicos__tiene_p_juridica=obj[0],anno=year)
			count_personeria = personeria_juridica.count()

			act_perso_juridica = filtro.filter(aspectos_juridicos__act_p_juridica=obj[0],anno=year)
			count_act_perso_juridica = act_perso_juridica.count()

			solvencia_tributaria = filtro.filter(aspectos_juridicos__solvencia_tributaria=obj[0],anno=year)
			count_solvencia = solvencia_tributaria.count()

			junta_directiva = filtro.filter(aspectos_juridicos__junta_directiva=obj[0],anno=year)
			count_junta_directiva = junta_directiva.count()

			socios = filtro.filter(aspectos_juridicos__lista_socios=obj[0],anno=year)
			count_socios = socios.count()

			lista = [saca_porcentajes(count_personeria,count_org,False),
					saca_porcentajes(count_act_perso_juridica,count_org,False),
					saca_porcentajes(count_solvencia,count_org,False),
					saca_porcentajes(count_junta_directiva,count_org,False),
					saca_porcentajes(count_socios,count_org,False)]

			lista_org = [personeria_juridica,act_perso_juridica,solvencia_tributaria,junta_directiva,socios]

			aspectos_juridicos[obj[1]] = lista
			tabla_aspectos_juridicos[obj[1]] = lista_org

		#conteo hombre y mujeres por status
		lista_status = Status.objects.all()
		lista_hombres = []
		lista_mujeres = []
		graf_bar_status = {}
		graf_pie_status = {}
		mujeres_pie = 0
		hombres_pie = 0
		org_by_status = {}
		for obj in Status.objects.all():
			#organizaciones por status 
			name = filtro.filter(organizacion__status=obj,anno=year)
			org_by_status[obj] = name

			#grafico de barras ---------------------------------------------------------
			mujeres_bar = filtro.filter(organizacion__status=obj,anno=year).aggregate(total = Sum('aspectos_juridicos__mujeres'))['total']
			if mujeres_bar == None:
				 mujeres_bar = 0

			hombres_bar = filtro.filter(organizacion__status=obj,anno=year).aggregate(total = Sum('aspectos_juridicos__hombres'))['total']  
			if hombres_bar == None:
				 hombres_bar = 0

			lista_hombres.append([obj,hombres_bar])
			lista_mujeres.append([obj,mujeres_bar])
			#grafico de pastel #-----------------------------------------------------------
			mujeres = filtro.filter(organizacion__status=obj,anno=year).aggregate(total = Sum('aspectos_juridicos__mujeres'))['total']
			if mujeres == None:
				mujeres = 0
				mujeres_pie += mujeres
			else:
				mujeres_pie += mujeres

			hombres = filtro.filter(organizacion__status=obj,anno=year).aggregate(total = Sum('aspectos_juridicos__hombres'))['total']
			if hombres == None:
				hombres = 0
				hombres_pie += hombres
			else:
				hombres_pie += hombres

		total = hombres_pie + mujeres_pie
		graf_bar_status['Hombres'] = lista_hombres
		graf_bar_status['Mujeres'] = lista_mujeres

		graf_pie_status['Hombres'] = saca_porcentajes(hombres_pie,total,False)
		graf_pie_status['Mujeres'] = saca_porcentajes(mujeres_pie,total,False)

		anno[year] = (status,org_by_status,graf_bar_status,graf_pie_status,aspectos_juridicos,tabla_aspectos_juridicos)

	return render(request,template,locals())

@login_required
def documentacion(request,template='organizacion/documentacion.html'):
	filtro = _queryset_filtrado(request)

	organizaciones = filtro.distinct('organizacion__nombre').count()
	anno = collections.OrderedDict()
	anios_list = filtro.order_by('anno').values_list('anno', flat=True).distinct('anno')

	for year in anios_list:
		documentacion = {}
		tabla_documantacion = {}
		count_org = filtro.filter(anno=year).distinct('organizacion__nombre').count()
		for x in SI_NO_CHOICES:
			documentos = {}
			tabla_documentos = {}
			for obj in DOCUMENTOS_CHOICES:
				result = filtro.filter(documentacion__documentos=obj[0],documentacion__si_no=x[0],anno=year)
				count_result = result.count()
				documentos[obj[1]] = saca_porcentajes(count_result,count_org,False)
				tabla_documentos[obj[1]] = result
			
			documentacion[x[1]] = documentos
			tabla_documantacion[x[1]] = tabla_documentos

		anno[year] = (documentacion,tabla_documantacion)

	return render(request,template,locals())

@login_required
def datos_productivos(request,template="organizacion/datos_productivos.html"):
	filtro = _queryset_filtrado(request)

	organizaciones = filtro.distinct('organizacion__nombre').count()
	anno = collections.OrderedDict()
	anios_list = filtro.order_by('anno').values_list('anno', flat=True).distinct('anno')

	for year in anios_list:
		count_org = filtro.filter(anno=year).distinct('organizacion__nombre').count()
		#socios y socias de cacao
		try:
			socias = int(filtro.filter(anno=year).aggregate(socias=Avg('datos_productivos__socias'))['socias'])
		except:
			socias = 0

		try:
			socios = int(filtro.filter(anno=year).aggregate(socios=Avg('datos_productivos__socios'))['socios'])
		except:
			socios = 0

		#pre-socios y pre-socias
		try:
			pre_socias = int(filtro.filter(anno=year).aggregate(pre_socias=Avg('datos_productivos__pre_socias'))['pre_socias'])
		except:
			pre_socias = 0

		try:
			pre_socios = int(filtro.filter(anno=year).aggregate(pre_socios=Avg('datos_productivos__pre_socios'))['pre_socios'])
		except:
			pre_socios = 0

		#totales------------------------------------------------------------------------
		total_areas_socios = filtro.filter(anno=year).aggregate(area_total=Sum('datos_productivos__area_total'))['area_total']
		total_areas_organico = filtro.filter(anno=year).aggregate(area_total=Sum('datos_productivos__area_cert_organico'))['area_total']
		total_areas_convencional = filtro.filter(anno=year).aggregate(area_total=Sum('datos_productivos__area_convencional'))['area_total']
		#end totales--------------------------------------------------------------------

		#Rendimiento promedio en baba y seco-------------------------------------------
		frec1,frec2,frec3,frec4,frec5 = 0,0,0,0,0
		frec1_s,frec2_s,frec3_s,frec4_s,frec5_s = 0,0,0,0,0

		rendimiento = collections.OrderedDict()

		avg_rend_baba = filtro.filter(anno=year).aggregate(baba=Avg('datos_productivos__cacao_baba'))['baba']
		avg_rend_seco = filtro.filter(anno=year).aggregate(seco=Avg('datos_productivos__cacao_seco'))['seco']

		for obj in filtro.filter(anno=year).values_list('datos_productivos__cacao_baba', flat=True):
			if obj >= 1 and obj <= 10:
				frec1 += 1
			if obj > 10 and obj <= 20:
				frec2 += 1
			if obj > 20 and obj <= 30:
				frec3 += 1
			if obj > 30 and obj <= 40:
				frec4 += 1
			if obj > 40:
				frec5 += 1

		total_frecue_rend_baba = frec1 + frec2 + frec3 + frec4 + frec5

		for obj in filtro.filter(anno=year).values_list('datos_productivos__cacao_seco', flat=True):
			if obj >= 1 and obj <= 10:
				frec1_s += 1
			if obj > 10 and obj <= 20:
				frec2_s += 1
			if obj > 20 and obj <= 30:
				frec3_s += 1
			if obj > 30 and obj <= 40:
				frec4_s += 1
			if obj > 40:
				frec5_s += 1

		total_frecue_rend_seco = frec1_s + frec2_s + frec3_s + frec4_s + frec5_s

		#rangos area dic
		rendimiento['1-10 qq'] = (frec1,saca_porcentajes(frec1,total_frecue_rend_baba,False),
										frec1_s,saca_porcentajes(frec1_s,total_frecue_rend_seco,False))

		rendimiento['11-20 qq'] = (frec2,saca_porcentajes(frec2,total_frecue_rend_baba,False),
										frec2_s,saca_porcentajes(frec2_s,total_frecue_rend_seco,False))

		rendimiento['21-30 qq'] = (frec3,saca_porcentajes(frec3,total_frecue_rend_baba,False),
										frec3_s,saca_porcentajes(frec3_s,total_frecue_rend_seco,False))

		rendimiento['31-40 qq'] = (frec4,saca_porcentajes(frec4,total_frecue_rend_baba,False),
										frec4_s,saca_porcentajes(frec4_s,total_frecue_rend_seco,False))

		rendimiento['> 40 qq'] = (frec5,saca_porcentajes(frec5,total_frecue_rend_baba,False),
										frec5_s,saca_porcentajes(frec5_s,total_frecue_rend_seco,False))


		anno[year] = (socias,socios,pre_socias,pre_socios,total_areas_socios,total_areas_organico,total_areas_convencional,
						avg_rend_baba,rendimiento,total_frecue_rend_baba,avg_rend_seco,total_frecue_rend_seco)

	return render(request,template,locals())

@login_required
def infraestructura(request,template="organizacion/infraestructura.html"):
	filtro = _queryset_filtrado(request)

	organizaciones = filtro.distinct('organizacion__nombre').count()
	anno = collections.OrderedDict()
	anios_list = filtro.order_by('anno').values_list('anno', flat=True).distinct('anno')

	for year in anios_list:
		count_org = filtro.filter(anno=year).distinct('organizacion__nombre').count()
		#Infraestructura y maquinaria--------------------------------------------------
		infraestructura = []
		tabla_infraestructura = []
		for obj in INFRAESTRUCTURA_CHOICES:
			#tabla capacidad de las instalaciones -------------------------------------
			tienen = filtro.filter(infraestructura__tipo=obj[0],anno=year).count()
			no_tiene = count_org - tienen

			estado = []			
			for x in ESTADO_CHOICES:
				conteo = filtro.filter(infraestructura__tipo=obj[0],infraestructura__estado=x[0],anno=year).count()
				estado.append(saca_porcentajes(conteo,tienen,False)) 

			if obj[0] == 7:
				capacidad = "---"
				avg_capacidad = "---"
			else:
				capacidad = filtro.filter(infraestructura__tipo=obj[0],anno=year).aggregate(total=Sum('infraestructura__capacidad'))['total']
				avg_capacidad = filtro.filter(infraestructura__tipo=obj[0],anno=year).aggregate(total=Avg('infraestructura__capacidad'))['total']
				
				if capacidad == None:
					capacidad = 0

				if avg_capacidad == None:
					avg_capacidad = 0

			tabla_infraestructura.append((obj[1],tienen,no_tiene,estado,capacidad,avg_capacidad))

		anno[year] = tabla_infraestructura

	return render(request,template,locals())

@login_required
def comercializacion_organizaciones(request,template="organizacion/comercializacion.html"):
	filtro = _queryset_filtrado(request)

	organizaciones = filtro.distinct('organizacion__nombre').count()
	anno = collections.OrderedDict()
	anios_list = filtro.order_by('anno').values_list('anno', flat=True).distinct('anno')

	for year in anios_list:
		count_org = filtro.filter(anno=year).distinct('organizacion__nombre').count()
		
		#tabla totales-----------------------------------------------------------------
		cacao_baba = filtro.filter(anno=year).aggregate(total=Sum('comercializacion_org__cacao_baba_acopiado'))['total']
		avg_cacao_baba = filtro.filter(anno=year).aggregate(total=Avg('comercializacion_org__cacao_baba_acopiado'))['total']

		cacao_seco = filtro.filter(anno=year).aggregate(total=Sum('comercializacion_org__cacao_seco_comercializado'))['total']
		avg_cacao_seco = filtro.filter(anno=year).aggregate(total=Avg('comercializacion_org__cacao_seco_comercializado'))['total']

		socios_cacao = filtro.filter(anno=year).aggregate(total=Sum('comercializacion_org__socios_cacao'))['total']
		avg_socios_cacao = filtro.filter(anno=year).aggregate(total=Avg('comercializacion_org__socios_cacao'))['total']

		no_socios = filtro.filter(anno=year).aggregate(total=Sum('comercializacion_org__productores_no_asociados'))['total']
		avg_no_socios = filtro.filter(anno=year).aggregate(total=Avg('comercializacion_org__productores_no_asociados'))['total']

		#Tipo de producto comercializado-----------------------------------------------
		tipo_producto = {}
		for obj in TIPO_PROD_CHOICES:
			if obj[0] != 3:
				count = filtro.filter(anno=year,comercializacion_org__tipo_producto=obj[0]).count()
				tipo_producto[obj[1]] = count 

		#Certificación utilizada para comercializar cacao -----------------------------
		certificacion_cacao = {}
		for obj in TIPO_MERCADO_CHOICES:
			conteo = filtro.filter(comercializacion_org__tipo_mercado__contains=obj[0],anno=year).count()
			certificacion_cacao[obj[1]] = saca_porcentajes(conteo,count_org,False)
		
		#Destino de la producción de cacao---------------------------------------------
		destino_produccion = {}
		for obj in DESTINO_CHOICES:
			conteo = filtro.filter(comercializacion_org__destino_produccion__contains=obj[0],anno=year).count()
			destino_produccion[obj[1]] = saca_porcentajes(conteo,count_org,False)

		anno[year] = (tipo_producto,certificacion_cacao,destino_produccion,cacao_baba,avg_cacao_baba,cacao_seco,
						avg_cacao_seco,socios_cacao,avg_socios_cacao,no_socios,avg_no_socios)

	return render(request,template,locals())

@login_required
def financiamiento(request,template="organizacion/financiamiento.html"):
	filtro = _queryset_filtrado(request)

	organizaciones = filtro.distinct('organizacion__nombre').count()
	anno = collections.OrderedDict()
	anios_list = filtro.order_by('anno').values_list('anno', flat=True).distinct('anno')

	for year in anios_list:
		count_org = filtro.filter(anno=year).distinct('organizacion__nombre').count()
		#Acceso a financiamiento para el acopio y comercialización---------------------
		financiamiento_cacao = {}
		for obj in ACOPIO_COMERCIO_CHOICES:
			conteo = filtro.filter(acopio_comercio__seleccion__contains=obj[0],anno=year).count()
			financiamiento_cacao[obj[1]] = saca_porcentajes(conteo,count_org,False)

		#grafico conteo financiamiento
		si_acceso = filtro.filter(anno=year).count()
		no_acceso = count_org - si_acceso 

		#diccionario de los años ------------------------------------------------------
		anno[year] = (financiamiento_cacao,si_acceso,no_acceso)

	return render(request,template,locals())

@login_required
def lista_organizaciones(request,template='organizacion/lista_organizaciones.html'):
	filtro = _queryset_filtrado(request)
	organizaciones = filtro.distinct('organizacion__nombre').count()

	org = filtro.distinct('organizacion__nombre')

	return render(request,template,locals())

def orgdashboard(request,template="organizacion/dashboard.html"):
	filtro = _queryset_filtrado(request)
	organizaciones = filtro.distinct('organizacion__nombre').count()
		
	return render(request, template, locals())

#ajax filtros
def get_munis_org(request):
	'''Metodo para obtener los municipios via Ajax segun los departamentos selectos'''
	ids = request.GET.get('ids', '')
	dicc = {}
	resultado = []
	if ids:
		lista = ids.split(',')
		for id in lista:
			try:
				encuesta = Encuesta_Org.objects.all().distinct().values_list('organizacion__municipio__id', flat=True)
				departamento = Departamento.objects.get(pk=id)
				municipios = Municipio.objects.filter(departamento__id=departamento.pk,id__in=encuesta).order_by('nombre')
				lista1 = []
				for municipio in municipios:
					muni = {}
					muni['id'] = municipio.pk
					muni['nombre'] = municipio.nombre
					lista1.append(muni)
					dicc[departamento.nombre] = lista1
			except:
				pass

	#filtrar segun la organizacion seleccionada
	org_ids = request.GET.get('org_ids', '')
	if org_ids:
		lista = org_ids.split(',')
		municipios = [encuesta.municipio for encuesta in Encuesta.objects.filter(organizacion__id__in=lista)]
		#crear los keys en el dicc para evitar KeyError
		for municipio in municipios:
			dicc[municipio.departamento.nombre] = []

		#agrupar municipios por departamento padre
		for municipio in municipios:
			muni = {'id': municipio.id, 'nombre': municipio.nombre}
			if not muni in dicc[municipio.departamento.nombre]:
				dicc[municipio.departamento.nombre].append(muni)

	resultado.append(dicc)

	return HttpResponse(simplejson.dumps(resultado), content_type='application/json')

def get_comunies(request):
	ids = request.GET.get('ids', '')
	if ids:
		lista = ids.split(',')
	results = []
	comunies = Comunidad.objects.filter(municipio__pk__in=lista).order_by('nombre').values('id', 'nombre')

	return HttpResponse(simplejson.dumps(list(comunies)), content_type='application/json')

#utils
def saca_porcentajes(dato, total, formato=True):
	if dato != None:
		try:
			porcentaje = (dato/float(total)) * 100 if total != None or total != 0 else 0
		except:
			return 0
		if formato:
			return porcentaje
		else:
			return '%.2f' % porcentaje
	else:
		return 0