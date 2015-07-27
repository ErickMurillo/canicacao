from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import *
import json as simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Sum, Count, Avg

# Create your views here.
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

	return Encuesta.objects.filter(**params)

def IndexView(request,template="index.html"):
	mujeres = Encuesta.objects.filter(persona__sexo='2').count()
	hombres = Encuesta.objects.filter(persona__sexo='1').count()
	area_cacao = Encuesta.objects.all().aggregate(area_cacao=Sum('area_cacao__area'))['area_cacao']
	produccion = Encuesta.objects.all().aggregate(total=Sum('produccion_cacao', 
													   		field="produccion_c_baba + produccion_c_seco + " + 
													   		"produccion_c_fermentado + produccion_c_organico"))['total']

	return render(request, template, locals())

def consulta(request,template="consulta.html"):
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


def dashboard(request,template='dashboard.html'):
	filtro = _queryset_filtrado(request)	

	familias = filtro.count()
	try:
		hombres = (filtro.filter(persona__sexo='1').count()/float(familias))*100
	except:
		hombres = 0 
	
	try:
		mujeres = (filtro.filter(persona__sexo='2').count()/float(familias))*100
	except:
		mujeres = 0 
	
	
	socio = filtro.filter(organizacion_asociada__socio='1').count()
	no_socio = filtro.filter(organizacion_asociada__socio='2').count()
	avg_cacao = filtro.aggregate(avg_cacao=Avg('area_cacao__area'))['avg_cacao']

	for x in filtro:
		organizaciones = Organizacion.objects.filter(encuesta=filtro).distinct().count()

	try:
		avg_area_productor = filtro.aggregate(sum_area=Sum('uso_tierra__area_total'))['sum_area'] / familias
	except:
		avg_area_productor = 0
	

	#graf volumen producido vs acopiado
	dic = {}
	for year in request.session['anno']:
		produccion = filtro.filter(anno=year).aggregate(total=Sum('produccion_cacao', 
													   field="produccion_c_baba + produccion_c_seco + " + 
													   "produccion_c_fermentado + produccion_c_organico"))['total']

		acopio = Organizacion.objects.filter(comercializacion_org__fecha=year).aggregate(total=Sum(
															'comercializacion_org__cacao_baba_acopiado'))['total']
		if produccion == None:
			produccion = 0

		if acopio == None:
			acopio = 0
			
		dic[year] = (produccion,acopio)

	####################################################################################################################
	#graf rendimiento socio
	rend_socio =  filtro.filter(organizacion_asociada__socio='1').aggregate(area_cacao=Sum('plantacion__area'))['area_cacao']
	baba_socio = filtro.filter(organizacion_asociada__socio='1').aggregate(cacao_baba_s=Sum('produccion_cacao__produccion_c_baba'))['cacao_baba_s']
	seco_socio = filtro.filter(organizacion_asociada__socio='1').aggregate(cacao_seco_s=Sum('produccion_cacao__produccion_c_seco'))['cacao_seco_s']
	fer_socio = filtro.filter(organizacion_asociada__socio='1').aggregate(cacao_fer_s=Sum('produccion_cacao__produccion_c_fermentado'))['cacao_fer_s']
	org_socio = filtro.filter(organizacion_asociada__socio='1').aggregate(cacao_org_s=Sum('produccion_cacao__produccion_c_organico'))['cacao_org_s']
	
	#graf rendimiento no socio
	rend_no_socio =  filtro.filter(organizacion_asociada__socio='2').aggregate(area_cacao=Sum('plantacion__area'))['area_cacao']
	baba_no_socio = filtro.filter(organizacion_asociada__socio='2').aggregate(cacao_baba=Sum('produccion_cacao__produccion_c_baba'))['cacao_baba']
	seco_no_socio = filtro.filter(organizacion_asociada__socio='2').aggregate(cacao_seco=Sum('produccion_cacao__produccion_c_seco'))['cacao_seco']
	fer_no_socio = filtro.filter(organizacion_asociada__socio='2').aggregate(cacao_fer=Sum('produccion_cacao__produccion_c_fermentado'))['cacao_fer']
	org_no_socio = filtro.filter(organizacion_asociada__socio='2').aggregate(cacao_org=Sum('produccion_cacao__produccion_c_organico'))['cacao_org']

	#resultado rendimiento
	#socio --------------------------------------------------
	try:
		s_result1 = rend_socio/float(baba_socio)
	except:
		s_result1 = 0
	
	try:
		s_result2 = rend_socio/float(seco_socio)
	except:
		s_result2 = 0

	try:
		s_result3 = rend_socio/float(fer_socio)
	except:
		s_result3 = 0

	try:
		s_result4 = rend_socio/float(org_socio)
	except:
		s_result4 = 0
	
	#no socio -----------------------------------------------
	try:
		ns_result1 = rend_no_socio/float(baba_no_socio)
	except:
		ns_result1 = 0

	try:
		ns_result2 = rend_no_socio/float(seco_no_socio)
	except:
		ns_result2 = 0

	try:
		ns_result3 = rend_no_socio/float(fer_no_socio)
	except:
		ns_result3 = 0

	try:
		ns_result4 = rend_no_socio/float(org_no_socio)
	except:
		ns_result4 = 0	

	return render(request, template, locals())

#nivel de educacion
def educacion(request,template='educacion.html'):
	filtro = _queryset_filtrado(request)

	tabla_educacion = []
	grafo = []
	suma = 0
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
		variable = round(saca_porcentajes(suma,objeto['num_total']))
		grafo.append([e[1],variable])
		fila = [e[1], objeto['num_total'],
                saca_porcentajes(objeto['no_leer'], objeto['num_total'], False),
                saca_porcentajes(objeto['p_incompleta'], objeto['num_total'], False),
                saca_porcentajes(objeto['p_completa'], objeto['num_total'], False),
                saca_porcentajes(objeto['s_incompleta'], objeto['num_total'], False),
                saca_porcentajes(objeto['bachiller'], objeto['num_total'], False),
                saca_porcentajes(objeto['universitario'], objeto['num_total'], False),
                saca_porcentajes(objeto['f_comunidad'], objeto['num_total'], False)]
		tabla_educacion.append(fila)
	print grafo

	return render(request, template, locals())

def propiedad(request,template='propiedad.html'):
	filtro = _queryset_filtrado(request)

	familias = filtro.count()

	count_si = filtro.filter(tenencia_propiedad__dueno_propiedad='1').count()
	count_no = filtro.filter(tenencia_propiedad__dueno_propiedad='2').count()
	dueno = (count_si/float(familias))*100
	no_dueno = (count_no/float(familias))*100


	dic = {}
	for e in PROPIEDAD_CHOICE:
		for x in e:	
			objeto = filtro.filter(tenencia_propiedad__si=e[0]).count()
		try:
			dic[x] = (objeto/count_si)*100
		except:
			dic[x] = 0

	dic2 = {}
	for x in Situacion.objects.all():
		objeto = filtro.filter(tenencia_propiedad__no=x).count()
		try:
			dic2[x] = (objeto/count_no)*100
		except:
			dic2[x] = 0
		

	return render(request, template, locals())

def uso_tierra(request,template='uso_tierra.html'):
	filtro = _queryset_filtrado(request)

	total = filtro.aggregate(area_total=Sum('uso_tierra__area_total'))['area_total']

	#grafico numero de manzanas
	bosque = filtro.aggregate(bosque=Sum('uso_tierra__bosque'))['bosque']
	tacotal = filtro.aggregate(tacotal=Sum('uso_tierra__tacotal'))['tacotal']
	cultivo_anual = filtro.aggregate(cultivo_anual=Sum('uso_tierra__cultivo_anual'))['cultivo_anual']
	plantacion_forestal = filtro.aggregate(plantacion_forestal=Sum('uso_tierra__plantacion_forestal'))['plantacion_forestal']
	area_pasto_abierto = filtro.aggregate(area_pasto_abierto=Sum('uso_tierra__area_pasto_abierto'))['area_pasto_abierto']
	area_pasto_arboles = filtro.aggregate(area_pasto_arboles=Sum('uso_tierra__area_pasto_arboles'))['area_pasto_arboles']
	cultivo_perenne = filtro.aggregate(cultivo_perenne=Sum('uso_tierra__cultivo_perenne'))['cultivo_perenne']
	cultivo_semi_perenne = filtro.aggregate(cultivo_semi_perenne=Sum('uso_tierra__cultivo_semi_perenne'))['cultivo_semi_perenne']
	cacao =  filtro.aggregate(cacao=Sum('uso_tierra__cacao'))['cacao']
	huerto_mixto_cacao = filtro.aggregate(huerto_mixto_cacao=Sum('uso_tierra__huerto_mixto_cacao'))['huerto_mixto_cacao']
	otros = filtro.aggregate(otros=Sum('uso_tierra__otros'))['otros']

	#tabla distribucion de la tierra
	t_bosque = (bosque/total) * 100
	t_tacotal = (tacotal/total) * 100
	t_cultivo_anual = (cultivo_anual/total) * 100
	t_plantacion_forestal = (plantacion_forestal/total) * 100
	t_area_pasto_abierto = (area_pasto_abierto/total) * 100
	t_area_pasto_arboles = (area_pasto_arboles/total) * 100
	t_cultivo_perenne = (cultivo_perenne/total) * 100
	t_cultivo_semi_perenne = (cultivo_semi_perenne/total) * 100
	t_cacao = (cacao/total) * 100
	t_huerto_mixto_cacao = (huerto_mixto_cacao/total) * 100
	t_otros = (otros/total) * 100

	return render(request, template, locals())

def produccion(request,template='produccion.html'):
	filtro = _queryset_filtrado(request)

	baba = filtro.aggregate(baba=Sum('produccion_cacao__produccion_c_baba'))['baba']
	seco = filtro.aggregate(seco=Sum('produccion_cacao__produccion_c_seco'))['seco']
	fermentado = filtro.aggregate(fermentado=Sum('produccion_cacao__produccion_c_fermentado'))['fermentado']
	organico = filtro.aggregate(organico=Sum('produccion_cacao__produccion_c_organico'))['organico']

	#baba = Produccion_Cacao.objects.filter(encuesta=filtro).aggregate(baba=Sum('produccion_c_baba'))['baba']

	# years = []
	# for x in Produccion_Cacao.objects.filter(encuesta=filtro):
	# 	for y in x.meses_produccion:
	# 		print y
	return render(request, template, locals())

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
        return HttpResponse(serializado, content_type='application/json')

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
                departamento = Departamento.objects.get(pk=id)
                municipios = Municipio.objects.filter(departamento__id=departamento.pk).order_by('nombre')
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

def get_organizacion(request):
    
    return render(request, "organizacion.html")

def get_org_detail(request):
    
    return render(request, "orgdetail.html")