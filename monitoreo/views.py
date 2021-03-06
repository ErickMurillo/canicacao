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

def _queryset_filtrado(request):
	params = {}

	if request.session['anno']:
		params['anno__in'] = request.session['anno']

	if request.session['departamento']:
		if not request.session['municipio']:
			municipios = Municipio.objects.filter(departamento__in=request.session['departamento'])
			params['persona__comunidad__municipio__in'] = municipios
		else:
			if request.session['comunidad']:
				params['persona__comunidad__in'] = request.session['comunidad']
			else:
				params['persona__comunidad__municipio__in'] = request.session['municipio']

	if request.session['organizacion']:
		params['organizacion'] = request.session['organizacion']

	if request.session['socio']:
		params['organizacion_asociada__socio'] = request.session['socio']


	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	return Encuesta.objects.filter(**params).order_by('anno')

@login_required
def IndexView(request,template="monitoreo/index.html"):
	hectarea = 0.7050
	tonelada = 0.045351474

	mujeres = Encuesta.objects.filter(persona__sexo='2').count()
	hombres = Encuesta.objects.filter(persona__sexo='1').count()
	area_cacao = (Encuesta.objects.all().aggregate(area_cacao=Sum('area_cacao__area'))['area_cacao']) * hectarea
	organizaciones = Encuesta_Org.objects.all().distinct('organizacion').count()

	produccion_seco = Encuesta.objects.all().aggregate(total=Sum('produccion_cacao__produccion_c_seco'))['total']
	if produccion_seco == None:
		produccion_seco = 0

	produccion_fermentado = Encuesta.objects.all().aggregate(total=Sum('produccion_cacao__produccion_c_fermentado'))['total']
	if produccion_fermentado == None:
		produccion_fermentado = 0

	produccion_organico = Encuesta.objects.all().aggregate(total=Sum('produccion_cacao__produccion_c_organico'))['total']
	if produccion_organico == None:
		produccion_organico = 0

	produccion_baba = Encuesta.objects.all().aggregate(total=Sum('produccion_cacao__produccion_c_baba'))['total']
	if produccion_baba == None:
		produccion_baba = 0

	try:
		produccion_seco_total = produccion_seco  + (produccion_baba/3)
	except:
		produccion_seco_total = 0

	produccion = (produccion_fermentado + produccion_organico + produccion_seco_total) * tonelada

	return render(request, template, locals())

@login_required
def consulta(request,template="monitoreo/consulta.html"):
	if request.method == 'POST':
		mensaje = None
		form = EncuestaConsulta(request.POST)
		if form.is_valid():
			request.session['anno'] = form.cleaned_data['anno']
			request.session['departamento'] = form.cleaned_data['departamento']
			request.session['municipio'] = form.cleaned_data['municipio']
			request.session['comunidad'] = form.cleaned_data['comunidad']
			request.session['organizacion'] = form.cleaned_data['organizacion']
			request.session['socio'] = form.cleaned_data['socio']

			mensaje = "Todas las variables estan correctamente :)"
			request.session['activo'] = True
			centinela = 1

			return HttpResponseRedirect('/dashboard/')

		else:
			centinela = 0

	else:
		form = EncuestaConsulta()
		mensaje = "Existen alguno errores"
		centinela = 0
		try:
			del request.session['anno']
			del request.session['departamento']
			del request.session['municipio']
			del request.session['comunidad']
			del request.session['organizacion']
			del request.session['socio']
		except:
			pass

	return render(request, template, locals())

@login_required
def dashboard(request,template='monitoreo/dashboard.html'):
	filtro = _queryset_filtrado(request)
	#nuevas salidas

	#conversiones###############
	hectarea = 0.7050
	tonelada = 0.045351474
	#1 libra = 0.00045359237 toneladas
	libra_tonelada = 0.00045359237
	############################

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	anno = collections.OrderedDict()

	for year in request.session['anno']:
		familias_year = filtro.filter(anno=year).count()
		#areas de cacao por edad de plantacion -----------------------------------------------------------------
		areas = collections.OrderedDict()
		area_total = filtro.filter(anno=year).aggregate(area_total=Sum('plantacion__area'))['area_total']
		try:
			ha_area_total = area_total * hectarea
		except:
			ha_area_total = 0

		for obj in EDAD_PLANTA_CHOICES:
			conteo = filtro.filter(anno=year,plantacion__edad=obj[0]).aggregate(total=Sum('plantacion__area'))['total']
			if conteo == None:
				conteo = 0
			result = conteo * hectarea
			areas[obj[1]] = saca_porcentajes(result,ha_area_total,False)

		#total de produccion cacao ----------------------------------------------------------------------------
		produccion_seco = filtro.filter(anno=year).aggregate(total=Sum('produccion_cacao__produccion_c_seco'))['total']
		if produccion_seco == None:
			produccion_seco = 0

		produccion_fermentado = filtro.filter(anno=year).aggregate(total=Sum('produccion_cacao__produccion_c_fermentado'))['total']
		if produccion_fermentado == None:
			produccion_fermentado = 0

		produccion_organico = filtro.filter(anno=year).aggregate(total=Sum('produccion_cacao__produccion_c_organico'))['total']
		if produccion_organico == None:
			produccion_organico = 0

		produccion_baba = filtro.filter(anno=year).aggregate(total=Sum('produccion_cacao__produccion_c_baba'))['total']
		if produccion_baba == None:
			produccion_baba = 0

		try:
			produccion_seco_total = produccion_seco + (produccion_baba/3)
		except:
			produccion_seco_total = 0

		try:
			total_produccion = (produccion_fermentado + produccion_organico + produccion_seco_total) * tonelada
		except:
			total_produccion = 0

		#mapa cantidades producida x depto
		prod_depto = {}
		for depto in Departamento.objects.all():
			produccion_seco_depto = filtro.filter(anno=year,persona__departamento=depto).aggregate(total=Sum('produccion_cacao__produccion_c_seco'))['total']
			if produccion_seco_depto == None:
				produccion_seco_depto = 0

			produccion_fermentado_depto = filtro.filter(anno=year,persona__departamento=depto).aggregate(total=Sum('produccion_cacao__produccion_c_fermentado'))['total']
			if produccion_fermentado_depto == None:
				produccion_fermentado_depto = 0

			produccion_organico_depto = filtro.filter(anno=year,persona__departamento=depto).aggregate(total=Sum('produccion_cacao__produccion_c_organico'))['total']
			if produccion_organico_depto == None:
				produccion_organico_depto = 0

			produccion_baba_depto = filtro.filter(anno=year,persona__departamento=depto).aggregate(total=Sum('produccion_cacao__produccion_c_baba'))['total']
			if produccion_baba_depto == None:
				produccion_baba_depto = 0

			try:
				produccion_seco_total_depto = produccion_seco_depto + (produccion_baba_depto/3)
			except:
				produccion_seco_total_depto = 0

			try:
				total_produccion_depto = (produccion_fermentado_depto + produccion_organico_depto + produccion_seco_total_depto) * tonelada
			except:
				total_produccion_depto = 0

			if total_produccion_depto != 0:
				prod_depto[depto] = (depto.latitud_1,depto.longitud_1,total_produccion_depto)

		#produccion x tipo cacao grafico------------------------------------------------------------------------
		p_seco = saca_porcentajes((produccion_seco_total*tonelada),total_produccion,False)
		p_fermentado = saca_porcentajes((produccion_fermentado*tonelada),total_produccion,False)
		p_organico = saca_porcentajes((produccion_organico*tonelada),total_produccion,False)

		#rendimiento cacao kg x ha -----------------------------------------------------------------------------

		#areas certificadas------------------------------------------------
		area_prod_cert = filtro.filter(anno=year,plantacion__edad__in=[3,4,5],certificacion__cacao_certificado='1').aggregate(area_cacao=Sum('plantacion__area'))['area_cacao']
		if area_prod_cert == None:
			area_prod_cert = 0

		#areas no certificadas----------------------------------------------
		area_prod_no_cert = filtro.filter(anno=year,plantacion__edad__in=[3,4,5],certificacion__cacao_certificado='2').aggregate(area_cacao=Sum('plantacion__area'))['area_cacao']
		if area_prod_no_cert == None:
			area_prod_no_cert = 0

		#----------------------------------------------------------- --------
		baba = filtro.filter(anno=year,certificacion__cacao_certificado='1').aggregate(cacao_baba_s=Sum('produccion_cacao__produccion_c_baba'))['cacao_baba_s']
		if baba == None:
			baba = 0

		baba_no_cert = filtro.filter(anno=year,certificacion__cacao_certificado='2').aggregate(cacao_baba_s=Sum('produccion_cacao__produccion_c_baba'))['cacao_baba_s']
		if baba_no_cert == None:
			baba_no_cert = 0

		seco = filtro.filter(anno=year).aggregate(cacao_seco_s=Sum('produccion_cacao__produccion_c_seco'))['cacao_seco_s']
		if seco == None:
			seco = 0

		fermentado = filtro.filter(anno=year).aggregate(cacao_fer_s=Sum('produccion_cacao__produccion_c_fermentado'))['cacao_fer_s']
		if fermentado == None:
			fermentado = 0

		organico = filtro.filter(anno=year).aggregate(cacao_org_s=Sum('produccion_cacao__produccion_c_organico'))['cacao_org_s']
		if organico == None:
			organico = 0

		area_hectarea_cert = area_prod_cert * hectarea
		area_hectarea_no_cert = area_prod_no_cert * hectarea

		#conversion de qq a kg
		kg_fermentado = fermentado * 45.35
		kg_organico = organico * 45.35
		#----------------------------------

		try:
			rendimiento_seco = (baba * 100) / area_hectarea
		except:
			rendimiento_seco = 0

		try:
			rendimiento_fer = (baba_no_cert * 100) / area_hectarea_no_cert
		except:
			rendimiento_fer = 0

		try:
			rendimiento_org = (kg_organico * 100) / area_hectarea_cert
		except:
			rendimiento_org = 0

		#promedio areas de cacao x productor
		try:
			avg_cacao = (filtro.filter(anno=year).aggregate(avg_cacao=Avg('area_cacao__area'))['avg_cacao']) * hectarea
		except:
			avg_cacao = 0

		#socio, no socio
		try:
			socio = (filtro.filter(anno=year,organizacion_asociada__socio='1').count() / float(familias_year)) * 100
		except:
			socio = 0

		try:
			no_socio = (filtro.filter(anno=year,organizacion_asociada__socio='2').count() / float(familias_year)) * 100
		except:
			no_socio = 0

		#auto-consumo vs venta -----------------------------------------------------------------------------------------
		PRODUCTO_CHOICES = (
			(3,'Cacao en baba'),
			(4,'Cacao rojo sin fermentar'),
			(5,'Cacao fermentado'),
			# (6,'Chocolate artesanal'),
			# (7,'Cacao en polvo'),
			# (8,'Cacao procesado/ pinolillo'),
			# (9,'Cajeta de cacao'),
			# (10,'Pasta de cacao'),
			)

		try:
			auto_consumo1 = (filtro.filter(anno=year,comercializacion_cacao__producto__in=[4,5]).aggregate(total=Sum(
					'comercializacion_cacao__auto_consumo'))['total'] ) * tonelada
		except:
			auto_consumo1 = 0

		try:
			auto_consumo2 = (filtro.filter(anno=year,comercializacion_cacao__producto=3).aggregate(total=Sum(
					'comercializacion_cacao__auto_consumo'))['total'] ) * tonelada
		except:
			auto_consumo2 = 0

		auto_consumo = auto_consumo1 + auto_consumo2

		try:
			venta1 = (filtro.filter(anno=year,comercializacion_cacao__producto__in=[4,5]).aggregate(total=Sum(
					'comercializacion_cacao__venta'))['total']) * tonelada
		except:
			venta1 = 0

		try:
			venta2 = (filtro.filter(anno=year,comercializacion_cacao__producto=3).aggregate(total=Sum(
					'comercializacion_cacao__venta'))['total']) * tonelada
		except:
			venta2 = 0

		venta = venta1 + venta2


		#Venta por calidad de cacao en Tn -----------------------------------------------------------------------------------
		comercializacion = collections.OrderedDict()
		for obj in PRODUCTO_CHOICES:
			if obj[0] == 3:
				try:
					total = (filtro.filter(anno=year,comercializacion_cacao__producto=obj[0]).aggregate(total=Sum(
											'comercializacion_cacao__venta'))['total']) * tonelada
				except:
					total = 0
			else:
				try:
					total = (filtro.filter(anno=year,comercializacion_cacao__producto=obj[0]).aggregate(total=Sum(
							'comercializacion_cacao__venta'))['total']) * tonelada
				except:
					total = 0
			comercializacion[obj[1]] = total

		#destino de produccion
		destino_dic = collections.OrderedDict()
		lista = []
		for x in Comercializacion_Cacao.objects.filter(encuesta__anno=year):
			if x.quien_vende != None:
				for y in x.quien_vende:
					lista.append(int(y))

		list_count = len(lista)
		r1 = lista.count(3)
		r2 = lista.count(4)
		suma = r1 + r2
		for obj in QUIEN_VENDE_CHOICES:
			p = lista.count(obj[0])
			# if obj[0] == 3:
			#     destino_dic["Otros"] = saca_porcentajes(suma, list_count, False)
			# elif obj[0] != 4 and obj[0] != 3:
			destino_dic[obj[1]] = saca_porcentajes(p, list_count, False)

		#destino de produccion de las organizaciones
		destino_org_dic = {}
		lista_org = []
		for xz in Comercializacion_Org.objects.filter(encuesta__anno=year):
			for yz in xz.destino_produccion:
				lista_org.append(int(yz))

		list_count_org = len(lista_org)

		for obj_1 in DESTINO_CHOICES:
			p2 = lista_org.count(obj_1[0])
			destino_org_dic[obj_1[1]] = saca_porcentajes(p2, list_count_org, False)


		#diccionario todos los valores x anio

		anno[year] = (areas,total_produccion,rendimiento_seco,rendimiento_fer,rendimiento_org,
						p_seco,p_fermentado,p_organico,avg_cacao,socio,no_socio,auto_consumo,venta,
						comercializacion,prod_depto,destino_dic,destino_org_dic)

	return render(request, template, locals())

#nivel de educacion
@login_required
def educacion(request,template='monitoreo/educacion.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	tabla_educacion = []
	grafo = []
	grafo_hombres = []
	grafo_mujeres = []
	suma = 0
	lista_hombres = [1,3,5,7,9]
	lista_mujeres = [2,4,6,8]
	RANGOS_CHOICE = (
		(7,'Niños 0 a 12 años'),
		(8,'Niñas 0 a 12 años'),
		(5,'Hombre adoles. 13 a 18 años'),
		(6,'Mujer adoles. 13 a 18 años'),
		(3,'Hombre joven 19 a 30 años'),
		(4,'Mujer joven 19 a 30 años'),
		(1,'Hombres mayores 31 años'),
		(2,'Mujeres mayores 31 años'),
		(9,'Ancianos (> 64 años)'),
		)

	for e in RANGOS_CHOICE:
		objeto = filtro.filter(educacion__rango = e[0]).aggregate(num_total = Sum('educacion__numero_total'),
				no_leer = Sum('educacion__no_lee_ni_escribe'),
				p_incompleta = Sum('educacion__primaria_incompleta'),
				p_completa = Sum('educacion__primaria_completa'),
				s_incompleta = Sum('educacion__secundaria_incompleta'),
				bachiller = Sum('educacion__bachiller'),
				universitario = Sum('educacion__universitario_tecnico'),
				f_comunidad = Sum('educacion__viven_fuera'))
		try:
			suma = int(objeto['p_completa'] or 0) + int(objeto['s_incompleta'] or 0) + int(objeto['bachiller'] or 0) + int(objeto['universitario'] or 0)
		except:
			pass
		variables = round(saca_porcentajes(suma,objeto['num_total']))

		if e[0] in lista_hombres:
			grafo_hombres.append([e[1],variables])
		elif e[0] in lista_mujeres:
			grafo_mujeres.append([e[1],variables])
		#grafo.append([e[1],variables])

		fila = [e[1], objeto['num_total'],
				saca_porcentajes(objeto['no_leer'], objeto['num_total'], False),
				saca_porcentajes(objeto['p_incompleta'], objeto['num_total'], False),
				saca_porcentajes(objeto['p_completa'], objeto['num_total'], False),
				saca_porcentajes(objeto['s_incompleta'], objeto['num_total'], False),
				saca_porcentajes(objeto['bachiller'], objeto['num_total'], False),
				saca_porcentajes(objeto['universitario'], objeto['num_total'], False),
				saca_porcentajes(objeto['f_comunidad'], objeto['num_total'], False)]
		tabla_educacion.append(fila)

	return render(request, template, locals())

@login_required
def propiedad(request,template='monitoreo/propiedad.html'):
	filtro = _queryset_filtrado(request)


	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	count_si = filtro.filter(tenencia_propiedad__dueno_propiedad=1).count()

	count_no = filtro.filter(tenencia_propiedad__dueno_propiedad=2).count()

	dueno = saca_porcentajes(count_si,familias,False)
	no_dueno = saca_porcentajes(count_no,familias,False)

	dic2 = {}
	for x in Situacion.objects.exclude(nombre='Sin documento'):
		objeto1 = filtro.filter(tenencia_propiedad__no=x).count()
		dic2[x] = saca_porcentajes(objeto1,count_no,False)

	dic = {}
	for e in PROPIEDAD_CHOICE:
		for x in e:
			objeto = filtro.filter(tenencia_propiedad__si=e[0]).count()
			dic[e[1]] = saca_porcentajes(objeto,count_si,False)
	return render(request, template, locals())

@login_required
def uso_tierra(request,template='monitoreo/uso_tierra.html'):
	filtro = _queryset_filtrado(request)
	hectarea = 0.7050
	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	total = (filtro.aggregate(area_total=Sum('uso_tierra__area_total'))['area_total']) * hectarea

	#grafico numero de manzanas
	bosque = (filtro.aggregate(bosque=Sum('uso_tierra__bosque'))['bosque']) * hectarea
	tacotal = (filtro.aggregate(tacotal=Sum('uso_tierra__tacotal'))['tacotal']) * hectarea
	cultivo_anual = (filtro.aggregate(cultivo_anual=Sum('uso_tierra__cultivo_anual'))['cultivo_anual']) * hectarea
	plantacion_forestal = (filtro.aggregate(plantacion_forestal=Sum('uso_tierra__plantacion_forestal'))['plantacion_forestal']) * hectarea
	area_pasto_abierto = (filtro.aggregate(area_pasto_abierto=Sum('uso_tierra__area_pasto_abierto'))['area_pasto_abierto']) * hectarea
	area_pasto_arboles = (filtro.aggregate(area_pasto_arboles=Sum('uso_tierra__area_pasto_arboles'))['area_pasto_arboles']) * hectarea
	cultivo_semi_perenne = (filtro.aggregate(cultivo_semi_perenne=Sum('uso_tierra__cultivo_semi_perenne'))['cultivo_semi_perenne']) * hectarea
	cacao =  (filtro.aggregate(cacao=Sum('uso_tierra__cacao'))['cacao']) * hectarea
	huerto_mixto_cacao = (filtro.aggregate(huerto_mixto_cacao=Sum('uso_tierra__huerto_mixto_cacao'))['huerto_mixto_cacao']) * hectarea
	cafe = (filtro.aggregate(cafe=Sum('uso_tierra__cafe'))['cafe']) * hectarea

	cultivo_perenne = (filtro.aggregate(cultivo_perenne=Sum('uso_tierra__cultivo_perenne'))['cultivo_perenne']) * hectarea
	otros_sub = (filtro.aggregate(otros=Sum('uso_tierra__otros'))['otros']) * hectarea

	otros = otros_sub + cultivo_perenne

	#tabla distribucion de la tierra
	t_bosque = saca_porcentajes(bosque,total,False)
	t_tacotal = saca_porcentajes(tacotal,total,False)
	t_cultivo_anual = saca_porcentajes(cultivo_anual,total,False)
	t_plantacion_forestal = saca_porcentajes(plantacion_forestal,total,False)
	t_area_pasto_abierto = saca_porcentajes(area_pasto_abierto,total,False)
	t_area_pasto_arboles = saca_porcentajes(area_pasto_arboles,total,False)
	t_cultivo_perenne = float(saca_porcentajes(cultivo_perenne,total,False))
	t_cultivo_semi_perenne = saca_porcentajes(cultivo_semi_perenne,total,False)
	t_cacao = saca_porcentajes(cacao,total,False)
	t_huerto_mixto_cacao = saca_porcentajes(huerto_mixto_cacao,total,False)
	t_cafe = saca_porcentajes(cafe,total,False)
	t_otros_sub = float(saca_porcentajes(otros,total,False))
	t_otros = t_cultivo_perenne + t_otros_sub

	return render(request, template, locals())

@login_required
def produccion(request,template='monitoreo/produccion.html'):
	filtro = _queryset_filtrado(request)
	tonelada = 0.045351474

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	#baba = (filtro.aggregate(baba=Sum('produccion_cacao__produccion_c_baba'))['baba'] ) / 3
	seco = (filtro.aggregate(seco=Sum('produccion_cacao__produccion_c_seco'))['seco']) * tonelada
	fermentado = (filtro.aggregate(fermentado=Sum('produccion_cacao__produccion_c_fermentado'))['fermentado'] ) * tonelada
	organico = (filtro.aggregate(organico=Sum('produccion_cacao__produccion_c_organico'))['organico'] ) * tonelada

	#meses de produccion
	produccion = {}
	lista = []
	for obj in Produccion_Cacao.objects.filter(encuesta=filtro):
		if obj.meses_produccion != None:
			for x in obj.meses_produccion:
				lista.append(int(x))

	for mes in MESES_CHOICES:
		p2 = lista.count(mes[0])
		produccion[mes[1]] = p2

	#problemas produccion
	fertilidad = saca_porcentajes(filtro.aggregate(total=Count('problemas_cacao__fertilidad'))['total'],familias,False)
	arboles = saca_porcentajes(filtro.aggregate(total=Count('problemas_cacao__arboles'))['total'],familias,False)
	plantaciones = saca_porcentajes(filtro.aggregate(total=Count('problemas_cacao__plantaciones'))['total'],familias,False)
	plagas = saca_porcentajes(filtro.aggregate(total=Count('problemas_cacao__plagas'))['total'],familias,False)
	produccion_problemas = saca_porcentajes(filtro.aggregate(total=Count('problemas_cacao__produccion'))['total'],familias,False)
	mano_obra = saca_porcentajes(filtro.aggregate(total=Count('problemas_cacao__mano_obra'))['total'],familias,False)

	#tabla nueva-------------------------------------
	EDAD_PLANTA_CHOICES = (
		# (1,'Menor de un año'),
		# (2,'De 1 a 3 años'),
		(3,'De 4 a 10 años'),
		(4,'De 10 a 20 años'),
		(5,'Mayores de 20 años'),
	)
	edades = {}
	hectarea = 0.7050
	for obj in EDAD_PLANTA_CHOICES:
		area_total = (filtro.filter(plantacion__edad=obj[0]).aggregate(total=Sum('plantacion__area'))['total']) * hectarea
		#----------------------------------------------------------------------------------------------------
		numero_plantas = filtro.filter(plantacion__edad=obj[0]).aggregate(plantas =
											Sum('plantacion__numero_plantas'))['plantas']
		numero_plantas_ha = numero_plantas / area_total
		#----------------------------------------------------------------------------------------------------
		improductivas = filtro.filter(plantacion__edad=obj[0]).aggregate(improductivas =
											Sum('plantacion__numero_p_improductivas'))['improductivas']
		plant_improd = saca_porcentajes(improductivas,numero_plantas,False)
		#----------------------------------------------------------------------------------------------------
		semillas = filtro.filter(plantacion__edad=obj[0]).aggregate(semillas =
											Sum('plantacion__numero_p_semilla'))['semillas']
		plantas_semillas = saca_porcentajes(semillas,numero_plantas,False)
		#----------------------------------------------------------------------------------------------------
		injerto = filtro.filter(plantacion__edad=obj[0]).aggregate(injerto =
											Sum('plantacion__numero_p_injerto'))['injerto']
		plantas_injerto = saca_porcentajes(injerto,numero_plantas,False)
		#----------------------------------------------------------------------------------------------------

		edades[obj[1]] = (area_total, numero_plantas_ha, plant_improd, plantas_semillas, plantas_injerto)

	#promedio de inversion
	inversion_finca = filtro.aggregate(finca = Avg('certificacion__mant_area_finca'))['finca']
	inversion_cacao = filtro.aggregate(cacao = Avg('certificacion__mant_area_cacao'))['cacao']

	return render(request, template, locals())

@login_required
def riesgos(request,template='monitoreo/riesgos.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	riesgos = collections.OrderedDict()
	riesgos_tabla = collections.OrderedDict()
	for obj in RIESGOS_CHOICES:
		sequia = filtro.filter(fenomenos_naturales__sequia=obj[0]).count()
		innundacion = filtro.filter(fenomenos_naturales__innundacion=obj[0]).count()
		lluvia = filtro.filter(fenomenos_naturales__lluvia=obj[0]).count()
		viento = filtro.filter(fenomenos_naturales__viento=obj[0]).count()
		deslizamiento = filtro.filter(fenomenos_naturales__deslizamiento=obj[0]).count()

		riesgos[obj[1]] = (saca_porcentajes(sequia,familias,False),
							saca_porcentajes(innundacion,familias,False),
							saca_porcentajes(lluvia,familias,False),
							saca_porcentajes(viento,familias,False),
							saca_porcentajes(deslizamiento,familias,False))

		riesgos_tabla[obj[1]] = (sequia,innundacion,lluvia,viento,deslizamiento)


	plantas = collections.OrderedDict()
	for obj in P_IMPRODUCTIVAS_CHOICES:
		p_improduct = filtro.filter(razones_agricolas__plantas_improductivas=obj[0]).count()
		plantas[obj[1]] = saca_porcentajes(p_improduct,familias,False)

	plagas = {}
	for obj in SI_NO_CHOICES:
		plagas_enfermedades = filtro.filter(razones_agricolas__plagas_enfermedades=obj[0]).count()
		quemas = filtro.filter(razones_agricolas__quemas=obj[0]).count()

		plagas[obj[1]] = (saca_porcentajes(plagas_enfermedades,familias,False),
							saca_porcentajes(quemas,familias,False))

	mercados = {}
	for obj in SI_NO_CHOICES:
		bajo_precio = filtro.filter(razones_mercado__bajo_precio=obj[0]).count()
		falta_venta = filtro.filter(razones_mercado__falta_venta=obj[0]).count()
		estafa_contrato = filtro.filter(razones_mercado__estafa_contrato=obj[0]).count()
		calidad_producto = filtro.filter(razones_mercado__calidad_producto=obj[0]).count()

		mercados[obj[1]] = (saca_porcentajes(bajo_precio,familias,False),
							saca_porcentajes(falta_venta,familias,False),
							saca_porcentajes(estafa_contrato,familias,False),
							saca_porcentajes(calidad_producto,familias,False))

	inversion = {}
	for obj in SI_NO_CHOICES:
		invierte_cacao = filtro.filter(inversion__invierte_cacao=obj[0]).count()
		interes_invertrir = filtro.filter(inversion__interes_invertrir=obj[0]).count()
		falta_credito = filtro.filter(inversion__falta_credito=obj[0]).count()
		altos_intereses = filtro.filter(inversion__altos_intereses=obj[0]).count()
		robo_producto = filtro.filter(inversion__robo_producto=obj[0]).count()

		inversion[obj[1]] = (saca_porcentajes(invierte_cacao,familias,False),
							saca_porcentajes(interes_invertrir,familias,False),
							saca_porcentajes(falta_credito,familias,False),
							saca_porcentajes(altos_intereses,familias,False),
							saca_porcentajes(robo_producto,familias,False))

	#mitigacion de riesgos
	tabla_mitigacion = {}
	for k in SI_NO_CHOICES:
		monitoreo_plagas = filtro.filter(mitigacion_riesgos__monitoreo_plagas = k[0]).count()
		#------------------------------------------------------
		manejo_cultivo = filtro.filter(mitigacion_riesgos__manejo_cultivo = k[0]).count()
		#------------------------------------------------------
		manejo_recursos = filtro.filter(mitigacion_riesgos__manejo_recursos = k[0]).count()
		#------------------------------------------------------
		almacenamiento_agua = filtro.filter(mitigacion_riesgos__almacenamiento_agua = k[0]).count()
		#------------------------------------------------------
		distribucion_cacao = filtro.filter(mitigacion_riesgos__distribucion_cacao = k[0]).count()
		#------------------------------------------------------
		venta_cacao = filtro.filter(mitigacion_riesgos__venta_cacao = k[0]).count()
		#------------------------------------------------------
		d_tecnologia_secado = filtro.filter(mitigacion_riesgos__d_tecnologia_secado = k[0]).count()
		#
		tabla_mitigacion[k[1]] = (saca_porcentajes(monitoreo_plagas,familias,False),
								saca_porcentajes(manejo_cultivo,familias,False),
								saca_porcentajes(manejo_recursos,familias,False),
								saca_porcentajes(almacenamiento_agua,familias,False),
								# saca_porcentajes(distribucion_cacao,familias,False),
								saca_porcentajes(venta_cacao,familias,False),
								saca_porcentajes(d_tecnologia_secado,familias,False),
							)
	return render(request, template, locals())

@login_required
def comercializacion(request,template='monitoreo/comercializacion.html'):
	filtro = _queryset_filtrado(request)
	tonelada = 0.045351474
	kg = 0.453592
	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	PRODUCTO_CHOICES = (
		(1,'Mazorca de cacao (unidad)'),
		(2,'Semilla para siembra (unidad)'),
		(3,'Cacao en baba (t)'),
		(4,'Cacao rojo sin fermentar (t)'),
		(5,'Cacao fermentado (t)'),
		(6,'Chocolate artesanal (unidad)'),
		(7,'Cacao en polvo (kg)'),
		(8,'Cacao procesado/ pinolillo (kg)'),
		(9,'Cajeta de cacao (kg)'),
		(10,'Pasta de cacao (kg)'),
		(11,'Vino de cacao (lt)'),
	)

	tabla_productos = []
	lista_toneladas = [3,4,5]
	lista_kg = [7,8,9,10]
	for obj in PRODUCTO_CHOICES:
		producto = filtro.filter(comercializacion_cacao__producto=obj[0]).aggregate(
				auto_consumo=Sum('comercializacion_cacao__auto_consumo'),
				venta=Sum('comercializacion_cacao__venta'),
				precio_venta=Avg('comercializacion_cacao__precio_venta'))

		#validacion y formato float
		if producto['auto_consumo'] != None:
			if obj[0] in lista_toneladas:
				auto_consumo = producto['auto_consumo'] * tonelada
			elif obj[0] in lista_kg:
				auto_consumo = producto['auto_consumo'] * kg
			else:
				auto_consumo = producto['auto_consumo']
		else:
			auto_consumo = 0.0

		if producto['venta'] != None:
			if obj[0] in lista_toneladas:
				venta = producto['venta'] * tonelada
			elif obj[0] in lista_kg:
				venta = producto['venta'] * kg
			else:
				venta = producto['venta']
		else:
			venta = 0.0

		if producto['precio_venta'] != None:
			if obj[0] in lista_toneladas:
				precio_venta = producto['precio_venta'] * 22.05
			elif obj[0] in lista_kg:
				precio_venta = producto['precio_venta'] * 2.2
			else:
				precio_venta = producto['precio_venta']
		else:
			precio_venta = 0.0
		#-----------------------------------------------------------
		fila = [obj[1],auto_consumo,venta,precio_venta]

		tabla_productos.append(fila)
	distancia = filtro.aggregate(avg=Avg('distancia_comercio_cacao__distancia'))['avg']

	return render(request, template, locals())

@login_required
def genero(request,template='monitoreo/genero.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	genero = {}
	suma_total = 0
	for obj in Actividades_Produccion.objects.all():
		suma_total += filtro.filter(genero__actividades=obj).count()

	for obj in Actividades_Produccion.objects.all():
		mujer = filtro.filter(genero__actividades=obj).count()
		genero[obj] = saca_porcentajes(mujer,suma_total,False)

	#recibe ingresos x actividades
	count_genero = Genero.objects.filter(encuesta=filtro).count()
	dic = {}
	for obj in SI_NO_CHOICES:
		recibe_ing = filtro.filter(genero__ingresos=obj[0]).count()
		dic[obj[1]] = saca_porcentajes(recibe_ing,count_genero,False)

	avg_ingresos = filtro.aggregate(avg=Avg('genero__ingreso_mesual'))['avg']

	agricola = {}
	domestico = {}
	mujeres_con_ingresos = recibe_ing = filtro.filter(genero__ingresos=1).count()
	for x in Destino_Ingresos.objects.all():
		if x.id in [1,2,4,6,5,7,8,9]:
			destino = filtro.filter(genero__destino_ingresos_2=x).count()
			domestico[x] = saca_porcentajes(destino,mujeres_con_ingresos,False)
			# print destino
		else:
			destino = filtro.filter(genero__destino_ingresos_2=x).count()
			agricola[x] = saca_porcentajes(destino,mujeres_con_ingresos,False)

	#---------------------------------------------------------------------
	decisiones = {}
	lista = []
	for obj in Genero.objects.filter(encuesta=filtro):
		if obj.decisiones != None:
			for x in obj.decisiones:
				if x != '2':
					lista.append(int(x))

	DECISIONES_CHOICES = (
	(1,'Siembra'),
	#(2,'Cosecha de cacao'),
	(3,'Venta'),
	(4,'Uso de ingresos'),
	)

	for dec in DECISIONES_CHOICES:
		p2 = lista.count(dec[0])
		decisiones[dec[1]] = saca_porcentajes(p2,familias,False)

	#sobre otros ingresos de la mujer
	ganaderia = saca_porcentajes(filtro.aggregate(count=Count('genero_2__ganaderia'))['count'],familias,False)
	granos_basicos = saca_porcentajes(filtro.aggregate(count=Count('genero_2__granos_basicos'))['count'],familias,False)
	cacao = saca_porcentajes(filtro.aggregate(count=Count('genero_2__cacao'))['count'],familias,False)
	cafe = saca_porcentajes(filtro.aggregate(count=Count('genero_2__cafe'))['count'],familias,False)
	madera = saca_porcentajes(filtro.aggregate(count=Count('genero_2__madera'))['count'],familias,False)

	return render(request, template, locals())

@login_required
def reforestacion(request,template='monitoreo/reforestacion.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	frec_bosques = filtro.filter(reforestacion__enriquecimiento_bosques='1').count()
	bosques = saca_porcentajes(frec_bosques,familias,False)

	frec_agua = filtro.filter(reforestacion__proteccion_agua='1').count()
	agua = saca_porcentajes(frec_agua,familias,False)

	frec_cercas = filtro.filter(reforestacion__cercas_vivas='1').count()
	cercas_vivas = saca_porcentajes(frec_cercas,familias,False)

	frec_vivereos = filtro.filter(reforestacion__viveros='1').count()
	viveros = saca_porcentajes(frec_vivereos,familias,False)

	frec_siembra = filtro.filter(reforestacion__siembre_cacao='1').count()
	siembre_cacao = saca_porcentajes(frec_siembra,familias,False)

	frec_forestales = filtro.filter(reforestacion__forestales='1').count()
	forestales = saca_porcentajes(frec_forestales,familias,False)

	frec_potrero = filtro.filter(reforestacion__potrero='1').count()
	potrero = saca_porcentajes(frec_potrero,familias,False)

	frec_frutales = filtro.filter(reforestacion__frutales='1').count()
	frutales = saca_porcentajes(frec_frutales,familias,False)

	return render(request, template, locals())

@login_required
def organizacion_productiva(request,template='monitoreo/org_productiva.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	servicio_dic = {}
	for obj in Tipos_Servicio.objects.exclude(servicio='Empleo'):
		servicio = filtro.filter(organizacion_asociada__tipos_servicio=obj).count()
		servicio_dic[obj] = saca_porcentajes(servicio,familias,False)

	beneficio_dic = {}
	for x in Beneficios.objects.exclude(id=6):
		beneficio = filtro.filter(organizacion_asociada__beneficios=x).count()
		beneficio_dic[x] = saca_porcentajes(beneficio,familias,False)

	return render(request, template, locals())

@login_required
def capacitaciones(request,template='monitoreo/capacitaciones.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct('nombre').count()
	##############################################################

	lista_t = []
	for obj in Capacitaciones_Tecnicas.objects.filter(encuesta=filtro):
		for x in obj.opciones:
			lista_t.append(int(x))
	total = len(lista_t)

	dic = {}
	for obj in CAPACITACIONES_CHOICES:
		lista = []
		capacitaciones = {}
		for cap in Capacitaciones_Tecnicas.objects.filter(encuesta=filtro,capacitaciones=obj[0]):
			for x in cap.opciones:
				lista.append(int(x))
				conteo = 0
		for xz in OPCIONES_CAPACITACIONES_CHOICES:
			p2 = lista.count(xz[0])
			conteo += p2
			capacitaciones[xz[1]] = p2

		dic[obj[1]] = (capacitaciones,conteo,saca_porcentajes(conteo,total,False))

	capacitaciones_2 = {}

	for obj_1 in OPCIONES_CAPACITACIONES_CHOICES:
		p2 = lista_t.count(obj_1[0])
		capacitaciones_2[obj_1[1]] = saca_porcentajes(p2,total,False)

	#socioeconomicas------------------------------------------------------------------------------
	lista_1 = []
	for obj_socio in Capacitaciones_Socioeconomicas.objects.filter(encuesta=filtro):
		if obj_socio.opciones_socio != None:
			for x in obj_socio.opciones_socio:
				lista_1.append(int(x))
	total_1 = len(lista_1)

	dic_socio = {}
	for obj in CAPACITACIONES_SOCIO_CHOICES:
		lista_socio = []
		capacitaciones_socio = {}
		for cap_socio in Capacitaciones_Socioeconomicas.objects.filter(encuesta=filtro,capacitaciones_socio=obj[0]):
			if cap_socio.opciones_socio != None:
				for z in cap_socio.opciones_socio:
					lista_socio.append(int(z))

		conteo = 0
		for xc in OPCIONES_CAPACITACIONES_CHOICES:
			p = lista_socio.count(xc[0])
			capacitaciones_socio[xc[1]] = p
			conteo += p

		dic_socio[obj[1]] = (capacitaciones_socio,conteo,saca_porcentajes(conteo,total_1,False))


	capacitaciones_socio = {}

	for obj_1_socio in OPCIONES_CAPACITACIONES_CHOICES:
		p = lista_1.count(obj_1_socio[0])
		capacitaciones_socio[obj_1_socio[1]] = saca_porcentajes(p,total_1,False)

	return render(request, template, locals())

@login_required
def capacitaciones_socio(request,template = 'monitoreo/capacitaciones_socio.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo = '1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo = '2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta = filtro).distinct('nombre').count()
	##############################################################

	dic_socio = {}
	for obj in CAPACITACIONES_SOCIO_CHOICES:
		lista = []
		capacitaciones = {}
		for cap in Capacitaciones_Socioeconomicas.objects.filter(encuesta = filtro,capacitaciones_socio = obj[0]):
			if cap.opciones_socio != None:
				for x in cap.opciones_socio:
					lista.append(int(x))

		for xz in OPCIONES_CAPACITACIONES_CHOICES:
			p = lista.count(xz[0])
			capacitaciones[xz[1]] = p
		dic_socio[obj[1]] = capacitaciones


	capacitaciones_socio = {}
	lista_1 = []
	for obj in Capacitaciones_Socioeconomicas.objects.filter(encuesta = filtro):
		if obj.opciones_socio != None:
			for x in obj.opciones_socio:
				lista_1.append(int(x))

	for obj_1 in OPCIONES_CAPACITACIONES_CHOICES:
		p = lista_1.count(obj_1[0])
		capacitaciones_socio[obj_1[1]] = p

	return render(request, template, locals())

#SALIDAS CARLOS
@login_required
def caracterizacion_terreno(request,template = 'monitoreo/caracterizacion_terreno.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo = '1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo = '2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta = filtro).distinct('nombre').count()
	##############################################################

	#caracteristicas del terrenos
	tabla_textura = {}
	suma1 = filtro.filter(caracterizacion_terreno__textura_suelo = 5).aggregate(
					textura=Count('caracterizacion_terreno__textura_suelo'))['textura']
	suma2 = filtro.filter(caracterizacion_terreno__textura_suelo = 4).aggregate(
					textura=Count('caracterizacion_terreno__textura_suelo'))['textura']
	total = suma1 + suma2

	for k in TEXTURA_CHOICES:
		query = filtro.filter(caracterizacion_terreno__textura_suelo = k[0])
		frecuencia = query.count()
		if k[0] == 5:
			textura = total
			por_textura = saca_porcentajes(textura, familias)
			tabla_textura['Franco'] = {'textura':textura,'por_textura':por_textura}

		elif k[0] != 4 and k[0] != 5:
			textura = filtro.filter(caracterizacion_terreno__textura_suelo = k[0]).aggregate(
						textura=Count('caracterizacion_terreno__textura_suelo'))['textura']

			por_textura = saca_porcentajes(textura, familias)
			tabla_textura[k[1]] = {'textura':textura,'por_textura':por_textura}

	#pendientes
	tabla_pendiente = {}
	for k in PENDIENTE_CHOICES:
		query = filtro.filter(caracterizacion_terreno__pendiente_terreno = k[0])
		frecuencia = query.count()
		pendiente = filtro.filter(caracterizacion_terreno__pendiente_terreno = k[0]).aggregate(pendiente = Count('caracterizacion_terreno__pendiente_terreno'))['pendiente']
		por_pendiente = saca_porcentajes(pendiente, familias)
		tabla_pendiente[k[1]] = {'pendiente':pendiente,'por_pendiente':por_pendiente}

	#pendientes
	tabla_hojarasca = {}
	for k in HOJARASCA_CHOICES:
		query = filtro.filter(caracterizacion_terreno__contenido_hojarasca = k[0])
		frecuencia = query.count()
		horajasca = filtro.filter(caracterizacion_terreno__contenido_hojarasca = k[0]).aggregate(horajasca=Count('caracterizacion_terreno__contenido_hojarasca'))['horajasca']
		por_horajasca = saca_porcentajes(horajasca, familias)
		tabla_hojarasca[k[1]] = {'horajasca':horajasca,'por_horajasca':por_horajasca}

	#Profundo
	tabla_profundidad = {}
	for k in PROFUNDIDAD_CHOICES:
		query = filtro.filter(caracterizacion_terreno__porfundidad_suelo = k[0])
		frecuencia = query.count()
		profundidad = filtro.filter(caracterizacion_terreno__porfundidad_suelo = k[0]).aggregate(profundidad=Count('caracterizacion_terreno__porfundidad_suelo'))['profundidad']
		por_profundidad = saca_porcentajes(profundidad, familias)
		tabla_profundidad[k[1]] = {'profundidad':profundidad,'por_profundidad':por_profundidad}

	tabla_drenaje = {}
	for k in DRENAJE_CHOICES:
		query = filtro.filter(caracterizacion_terreno__drenaje_suelo = k[0])
		frecuencia = query.count()
		drenaje = filtro.filter(caracterizacion_terreno__drenaje_suelo = k[0]).aggregate(drenaje = Count('caracterizacion_terreno__drenaje_suelo'))['drenaje']
		por_drenaje = saca_porcentajes(drenaje, familias)
		tabla_drenaje[k[1]] = {'drenaje':drenaje,'por_drenaje':por_drenaje}

	return render(request, template, locals())

@login_required
def mitigacion_riesgos(request,template = 'monitoreo/mitigacion_riesgos.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo = '1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo = '2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta = filtro).distinct('nombre').count()
	##############################################################

	#caracteristicas del terrenos
	tabla_mitigacion = {}
	for k in SI_NO_CHOICES:
		monitoreo_plagas = filtro.filter(mitigacion_riesgos__monitoreo_plagas = k[0]).count()
		#------------------------------------------------------
		manejo_cultivo = filtro.filter(mitigacion_riesgos__manejo_cultivo = k[0]).count()
		#------------------------------------------------------
		manejo_recursos = filtro.filter(mitigacion_riesgos__manejo_recursos = k[0]).count()
		#------------------------------------------------------
		almacenamiento_agua = filtro.filter(mitigacion_riesgos__almacenamiento_agua = k[0]).count()
		#------------------------------------------------------
		distribucion_cacao = filtro.filter(mitigacion_riesgos__distribucion_cacao = k[0]).count()
		#------------------------------------------------------
		venta_cacao = filtro.filter(mitigacion_riesgos__venta_cacao = k[0]).count()
		#------------------------------------------------------
		d_tecnologia_secado = filtro.filter(mitigacion_riesgos__d_tecnologia_secado = k[0]).count()
		#
		tabla_mitigacion[k[1]] = (saca_porcentajes(monitoreo_plagas,familias,False),
								saca_porcentajes(manejo_cultivo,familias,False),
								saca_porcentajes(manejo_recursos,familias,False),
								saca_porcentajes(almacenamiento_agua,familias,False),
								saca_porcentajes(distribucion_cacao,familias,False),
								saca_porcentajes(venta_cacao,familias,False),
								saca_porcentajes(d_tecnologia_secado,familias,False),
							)
	return render(request, template, locals())

@login_required
def tipo_certificacion(request,template='monitoreo/tipo_certificacion.html'):
	filtro = _queryset_filtrado(request)

	##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo = '1').count()/float(familias))*100
	except:
		 hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo = '2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta = filtro).distinct('nombre').count()
	##############################################################

	#productores certificados y no certificados
	certificados = filtro.filter(certificacion__cacao_certificado = 1).count()
	no_certificados = filtro.filter(certificacion__cacao_certificado = 2).count()

	#No de productores con uno o más sellos
	conteo_1 = 0
	conteo_2 = 0
	conteo_3 = 0
	lista = []
	for obj in filtro:
		certificaciones = 0
		for x in Certificacion.objects.filter(cacao_certificado=1,encuesta=obj):
			for z in x.tipo.all():
				certificaciones += 1
		if certificaciones == 1:
			conteo_1 += 1
		elif certificaciones == 2:
			conteo_2 += 1
		elif certificaciones > 2:
			conteo_3 += 1
	lista.append([conteo_1, conteo_2, conteo_3])

	#tipo de certificacion
	tabla_certificacion = {}
	for k in Lista_Certificaciones.objects.all().exclude(nombre = 'Convencional'):
		tipos = filtro.filter(certificacion__tipo = k).count()
		tabla_certificacion[k.nombre] = saca_porcentajes(tipos,familias,False)

	#quien certifica
	quien_certifica = {}
	for obj in Quien_Certifica.objects.all():
		conteo = filtro.filter(certificacion__quien_certifica = obj).count()
		quien_certifica[obj] = conteo

	#quien paga la certificacion
	paga_certificacion = {}
	for obj in Paga_Certifica.objects.all():
		conteo = filtro.filter(certificacion__paga_certificacion = obj).count()
		paga_certificacion[obj] = conteo

	#costo certificacion
	costo_certificacion = filtro.aggregate(costo = Avg('certificacion__costo_certificacion'))['costo']

	return render(request, template, locals())

@login_required
def tecnicas_aplicadas(request,template = 'monitoreo/tecnicas_aplicadas.html'):
	filtro = _queryset_filtrado(request)

   ##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo = '1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo = '2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta = filtro).distinct('nombre').count()
	##############################################################

	#VVEROS----------------------------------------------------------------------
	viveros = collections.OrderedDict()
	lista_viveros = []
	for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
		if obj.viveros != None:
			for x in obj.viveros:
				lista_viveros.append(int(x))

	VIVEROS_CHOICES = (
		(4,'Selección de semilla'),
		(5,'Siembra de semilla'),
		(2,'Preparación del sustrato'),
		(7,'Control de malas hierba'),
		(8,'Fertilización orgánica'),
		(6,'Uso de riego'),
	)
	total = len(lista_viveros) - (lista_viveros.count(1) + lista_viveros.count(3))

	for op in VIVEROS_CHOICES:
		p2 = lista_viveros.count(op[0])
		viveros[op[1]] = saca_porcentajes(p2,total,False)

	#FERTILIZACION----------------------------------------------------------------------
	fertilizacion = collections.OrderedDict()
	lista_fertilizacion = []
	for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
		if obj.fertilizacion != None :
			for x in obj.fertilizacion:
				lista_fertilizacion.append(int(x))

	FERTILIZACION_CHOICES = (
		(7,'Urea'),
		(6,'Lombrihumus'),
		(5,'Triple cal'),
		(4,'Abono foliar'),
		(3,'Bocashi'),
		(2,'Gallinaza'),
		(1,'Estiércol'),
		(8,'Fertilizante completo'),
	)

	for op in FERTILIZACION_CHOICES:
		p2 = lista_fertilizacion.count(op[0])
		fertilizacion[op[1]] = saca_porcentajes(p2,len(lista_fertilizacion),False)

	#pract_manejo_fis----------------------------------------------------------------------
	pract_manejo_fis = collections.OrderedDict()
	lista_pract_manejo_fis = []
	for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
		if obj.pract_manejo_fis != None:
			for x in obj.pract_manejo_fis:
				lista_pract_manejo_fis.append(int(x))

	P_MANEJO_FIS_CHOICES = (
		(3,'Uso de productos naturales contra plagas'),
		(5,'Fungicidas'),
		(6,'Eliminación fruto enfermo'),
		(1,'Control de malas hierbas con machete'),
		(4,'Uso de productos naturales contra hongos'),
		(2,'Herbicidas'),
	)

	for op in P_MANEJO_FIS_CHOICES:
		p2 = lista_pract_manejo_fis.count(op[0])
		pract_manejo_fis[op[1]] = saca_porcentajes(p2,len(lista_pract_manejo_fis),False)

	#pract_manejo_prod----------------------------------------------------------------------
	pract_manejo_prod = collections.OrderedDict()
	lista_pract_manejo_prod = []
	for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
		if obj.pract_manejo_prod != None:
			for x in obj.pract_manejo_prod:
				lista_pract_manejo_prod.append(int(x))

	P_MANEJO_PROD_CHOICES = (
		(1,'Poda de formación'),
		(2,'Poda de mantenimiento'),
		(3,'Poda de renovación'),
		(4,'Regulación de sombra'),
	)

	for op in P_MANEJO_PROD_CHOICES:
		p2 = lista_pract_manejo_prod.count(op[0])
		pract_manejo_prod[op[1]] = saca_porcentajes(p2,len(lista_pract_manejo_prod),False)

	#pract_mejora_plat----------------------------------------------------------------------
	pract_mejora_plat = collections.OrderedDict()
	lista_pract_mejora_plat = []
	for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
		if obj.pract_mejora_plat != None:
			for x in obj.pract_mejora_plat:
				lista_pract_mejora_plat.append(int(x))

	P_MEJORA_PLANT_CHOICES = (
		(2,'Injertación'),
		(3,'Renovación con plantas injertas'),
		(1,'Selección de árboles superiores'),
		(4,'Enriquecimiento de áreas con plantas injertadas'),
	)

	for op in P_MEJORA_PLANT_CHOICES:
		p2 = lista_pract_mejora_plat.count(op[0])
		pract_mejora_plat[op[1]] = saca_porcentajes(p2,len(lista_pract_mejora_plat),False)

	#pract_manejo_post_c----------------------------------------------------------------------
	pract_manejo_post_c = collections.OrderedDict()
	lista_pract_manejo_post_c = []
	for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
		if obj.pract_manejo_post_c != None:
			for x in obj.pract_manejo_post_c:
				lista_pract_manejo_post_c.append(int(x))

	P_MANEJO_POST_C_CHOICES = (
		(8,'Lavado y secado'),
		(7,'Secado'),
		(1,'Selección por variedades'),
		(6,'Venta en baba a centro de acopio'),
		(2,'Selección de cacao en baba'),
		(3,'Fermentación en sacos'),
		(5,'Fermentación en cajillas'),
		(4,'Fermentación en cajones'),
	)

	for op in P_MANEJO_POST_C_CHOICES:
		p2 = lista_pract_manejo_post_c.count(op[0])
		pract_manejo_post_c[op[1]] = saca_porcentajes(p2,len(lista_pract_manejo_post_c),False)

	#dispone de centro de acopio de cacao------------------------------------------------
	centro_acopio = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(tecnicas_aplicadas__acopio_cacao = obj[0]).count()
		centro_acopio[obj[1]] = conteo

	#socio de alguna org q acopia cacao--------------------------------------------------
	socio_acopio = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(tecnicas_aplicadas__acopio_org = obj[0]).count()
		socio_acopio[obj[1]] = conteo

	return render(request, template, locals())

@login_required
def ampliar_areas_cacao(request,template='monitoreo/ampliar_areas_cacao.html'):
	filtro = _queryset_filtrado(request)

   ##############################################################
	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo = '1').count()/float(familias))*100
	except:
		hombres = 0
	try:
		mujeres = (filtro.filter(persona__sexo = '2').count()/float(familias))*100
	except:
		mujeres = 0
	organizaciones = Organizacion.objects.filter(encuesta = filtro).distinct('nombre').count()
	##############################################################

	ampliar_areas = {}
	for obj in SI_NO_CHOICES:
		conteo = filtro.filter(adicional__interes = obj[0]).count()
		ampliar_areas[obj[1]] = conteo

	hectarea = 0.7050
	areas_total = filtro.aggregate(total = Sum('adicional__cuanto'))['total'] * hectarea
	avg_areas = filtro.aggregate(avg = Avg('adicional__cuanto'))['avg'] * hectarea

	return render(request, template, locals())

#ajax filtros
def get_munis(request):
	'''Metodo para obtener los municipios via Ajax segun los departamentos selectos'''
	ids = request.GET.get('ids', '')
	dicc = {}
	resultado = []
	if ids:
		lista = ids.split(',')
		for id in lista:
			try:
				encuesta = Encuesta.objects.filter(persona__municipio__departamento__id=id).distinct().values_list('persona__municipio__id', flat=True)
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

def get_organi(request):
	ids = request.GET.get('ids', '')
	if ids:
		lista = ids.split(',')
	organizaciones = Organizacion.objects.filter(municipio__id__in = lista).order_by('nombre').values('id', 'siglas')

	return HttpResponse(simplejson.dumps(list(organizaciones)), content_type='application/json')

#obtener puntos en el mapa
def obtener_lista(request):
	if request.is_ajax():
		lista = []
		for objeto in Encuesta.objects.all():
			dicc = dict(nombre=objeto.persona.municipio.nombre, id=objeto.id,
						lon=float(objeto.persona.municipio.longitud),
						lat=float(objeto.persona.municipio.latitud)
						)
			lista.append(dicc)

		serializado = simplejson.dumps(lista)
		return HttpResponse(serializado, content_type = 'application/json')

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

def get_fecha(request):
	years = []
	for en in Encuesta.objects.order_by('anno').values_list('anno', flat=True):
		years.append((en))
	lista = sorted(set(years))
	return HttpResponse(simplejson.dumps(lista), content_type='application/javascript')

def hectarea(dato):
	if dato != None:
		try:
			total = dato*float(hectarea) if total != None or total != 0 else 0
		except:
			return 0
		if formato:
			return total
		else:
			return '%.2f' % total
	else:
		return 0

def sumarLista(lista):
	sum=0
	for i in range(0,len(lista)):
		sum=sum+lista[i]
	return sum
