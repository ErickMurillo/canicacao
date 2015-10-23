# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import *
import json as simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Sum, Count, Avg
import collections

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

def get_org_detail(request):
    
    return render(request, "organizacion/orgdetail.html")

def obtener_lista_org(request):
    if request.is_ajax():
        lista = []
        for objeto in Organizacion.objects.all():
            dicc = dict(nombre=objeto.municipio.nombre, id=objeto.id,
                        lon=float(objeto.municipio.longitud),
                        lat=float(objeto.municipio.latitud)
                        )
            lista.append(dicc)

        serializado = simplejson.dumps(lista)
        return HttpResponse(serializado, content_type='application/json')

def orgdashboard(request,template="organizacion/dashboard.html"):
    filtro = _queryset_filtrado(request)

    organizaciones = filtro.distinct('organizacion__nombre').count()

    #detalle_org = filtro.distinct('organizacion__nombre')

    anno = collections.OrderedDict()
    anno_org_names = collections.OrderedDict()

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

        #documentacion-----------------------------------------------------------------
        documentacion = {}
        tabla_documantacion = {}
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

        #pendiente revision de datos para establecer rangos
        #************************************************************************

        #Área establecida por sus socias y socios en cacao-------------------------------------
        frec1,frec2,frec3 = 0,0,0

        rangos_area = collections.OrderedDict()

        avg_area = filtro.filter(anno=year).aggregate(area_total=Avg('datos_productivos__area_total'))['area_total']

        for obj in filtro.filter(anno=year).values_list('datos_productivos__area_total', flat=True):
            if obj >= 1 and obj <= 5:
                frec1 += 1
            if obj >= 6 and obj <= 10:
                frec2 += 1
            if obj >= 11:
                frec3 += 1

        #rangos area dic
        rangos_area['1-5 mz'] = (frec1,saca_porcentajes(frec1,count_org,False))
        rangos_area['6-10 mz'] = (frec2,saca_porcentajes(frec2,count_org,False))
        rangos_area['> 11 mz'] = (frec3,saca_porcentajes(frec3,count_org,False))
        total_frecuencia_rangos = frec1 + frec2 + frec3

        #Área establecida de cacao orgánico ---------------------------------------------------
        frec1,frec2,frec3 = 0,0,0

        rangos_organico = collections.OrderedDict()

        avg_area_organico = filtro.filter(anno=year).aggregate(area_total=Avg('datos_productivos__area_cert_organico'))['area_total']

        for obj in filtro.filter(anno=year).values_list('datos_productivos__area_cert_organico', flat=True):
            if obj >= 1 and obj <= 5:
                frec1 += 1
            if obj >= 6 and obj <= 10:
                frec2 += 1
            if obj >= 11:
                frec3 += 1

        #rangos area dic
        rangos_organico['1-5 mz'] = (frec1,saca_porcentajes(frec1,count_org,False))
        rangos_organico['6-10 mz'] = (frec2,saca_porcentajes(frec2,count_org,False))
        rangos_organico['> 11 mz'] = (frec3,saca_porcentajes(frec3,count_org,False))
        total_frecuencia_organico = frec1 + frec2 + frec3

        #Área establecida de cacao convencional ---------------------------------------------------
        frec1,frec2,frec3 = 0,0,0

        rangos_convencional = collections.OrderedDict()

        avg_area_convencional = filtro.filter(anno=year).aggregate(area_total=Avg('datos_productivos__area_convencional'))['area_total']

        for obj in filtro.filter(anno=year).values_list('datos_productivos__area_convencional', flat=True):
            if obj >= 1 and obj <= 5:
                frec1 += 1
            if obj >= 6 and obj <= 10:
                frec2 += 1
            if obj >= 11:
                frec3 += 1

        #rangos area dic
        rangos_convencional['1-5 mz'] = (frec1,saca_porcentajes(frec1,count_org,False))
        rangos_convencional['6-10 mz'] = (frec2,saca_porcentajes(frec2,count_org,False))
        rangos_convencional['> 11 mz'] = (frec3,saca_porcentajes(frec3,count_org,False))
        total_frecuencia_convecional = frec1 + frec2 + frec3
        #************************************************************************

        #diccionario de los años
        anno[year] = (status,org_by_status,graf_bar_status,graf_pie_status,aspectos_juridicos,tabla_aspectos_juridicos,
                        documentacion,tabla_documantacion,socias,socios,pre_socias,pre_socios,rangos_area,
                        total_frecuencia_rangos,avg_area,rangos_organico,total_frecuencia_organico,avg_area_organico,
                        rangos_convencional,total_frecuencia_convecional,avg_area_convencional)
        #------------------------------------------------------------------------------- 

    areas_establecidas = filtro.aggregate(areas=Avg('datos_productivos__area_total'))['areas']
    if areas_establecidas == None:
        areas_establecidas = 0

    area_organico = filtro.aggregate(organico=Avg('datos_productivos__area_cert_organico'))['organico']
    if area_organico == None:
        area_organico = 0

    area_convencional = filtro.aggregate(convencional=Avg('datos_productivos__area_convencional'))['convencional']
    if area_convencional == None:
        area_convencional = 0
        
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