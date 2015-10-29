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

def get_org_detail(request,id=None,template="organizacion/orgdetail.html"):
    org = Organizacion.objects.get(id=id)
    return render(request,template,locals())

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
        frec1,frec2,frec3,frec4,frec5 = 0,0,0,0,0

        rangos_area = collections.OrderedDict()

        avg_area = filtro.filter(anno=year).aggregate(area_total=Avg('datos_productivos__area_total'))['area_total']

        for obj in filtro.filter(anno=year).values_list('datos_productivos__area_total', flat=True):
            if obj >= 1 and obj <= 250:
                frec1 += 1
            if obj > 250 and obj <= 500:
                frec2 += 1
            if obj > 500 and obj <= 750:
                frec3 += 1
            if obj > 750 and obj <= 1000:
                frec4 += 1
            if obj > 1000:
                frec5 += 1

        total_frecuencia_rangos = frec1 + frec2 + frec3 + frec4 + frec5
        #rangos area dic
        rangos_area['1-250 mz'] = (frec1,saca_porcentajes(frec1,total_frecuencia_rangos,False))
        rangos_area['251-500 mz'] = (frec2,saca_porcentajes(frec2,total_frecuencia_rangos,False))
        rangos_area['501-750 mz'] = (frec3,saca_porcentajes(frec3,total_frecuencia_rangos,False))
        rangos_area['751-1000 mz'] = (frec4,saca_porcentajes(frec4,total_frecuencia_rangos,False))
        rangos_area['> 1000 mz'] = (frec5,saca_porcentajes(frec5,total_frecuencia_rangos,False))

        #Área establecida de cacao orgánico ---------------------------------------------------
        frec1,frec2,frec3,frec4,frec5 = 0,0,0,0,0

        rangos_organico = collections.OrderedDict()

        avg_area_organico = filtro.filter(anno=year).aggregate(area_total=Avg('datos_productivos__area_cert_organico'))['area_total']

        for obj in filtro.filter(anno=year).values_list('datos_productivos__area_cert_organico', flat=True):
            if obj >= 1 and obj <= 150:
                frec1 += 1
            if obj > 150 and obj <= 300:
                frec2 += 1
            if obj > 300 and obj <= 450:
                frec3 += 1
            if obj > 450 and obj <= 600:
                frec4 += 1
            if obj > 600:
                frec5 += 1

        total_frecuencia_organico = frec1 + frec2 + frec3 + frec4 + frec5
        #rangos area dic
        rangos_organico['1-150 mz'] = (frec1,saca_porcentajes(frec1,total_frecuencia_organico,False))
        rangos_organico['151-300 mz'] = (frec2,saca_porcentajes(frec2,total_frecuencia_organico,False))
        rangos_organico['301-450 mz'] = (frec3,saca_porcentajes(frec3,total_frecuencia_organico,False))
        rangos_organico['451-600 mz'] = (frec4,saca_porcentajes(frec4,total_frecuencia_organico,False))
        rangos_organico['> 600 mz'] = (frec5,saca_porcentajes(frec5,total_frecuencia_organico,False))
        

        #Área establecida de cacao convencional ---------------------------------------------------
        frec1,frec2,frec3,frec4,frec5 = 0,0,0,0,0

        rangos_convencional = collections.OrderedDict()

        avg_area_convencional = filtro.filter(anno=year).aggregate(area_total=Avg('datos_productivos__area_convencional'))['area_total']

        for obj in filtro.filter(anno=year).values_list('datos_productivos__area_convencional', flat=True):
            if obj >= 1 and obj <= 150:
                frec1 += 1
            if obj > 150 and obj <= 300:
                frec2 += 1
            if obj > 300 and obj <= 450:
                frec3 += 1
            if obj > 450 and obj <= 600:
                frec4 += 1
            if obj > 600:
                frec5 += 1

        total_frecuencia_convecional = frec1 + frec2 + frec3 + frec4 + frec5

        #rangos area dic
        rangos_convencional['1-150 mz'] = (frec1,saca_porcentajes(frec1,total_frecuencia_convecional,False))
        rangos_convencional['151-300 mz'] = (frec2,saca_porcentajes(frec2,total_frecuencia_convecional,False))
        rangos_convencional['301-450 mz'] = (frec3,saca_porcentajes(frec3,total_frecuencia_convecional,False))
        rangos_convencional['451-600 mz'] = (frec4,saca_porcentajes(frec4,total_frecuencia_convecional,False))
        rangos_convencional['> 600 mz'] = (frec5,saca_porcentajes(frec5,total_frecuencia_convecional,False))
        #************************************************************************

        #Infraestructura y maquinaria
        infraestructura = {}
        tabla_infraestructura = []
        for obj in INFRAESTRUCTURA_CHOICES:
            #tabla capacidad de las instalaciones -------------------------------------
            instalaciones = filtro.filter(infraestructura__tipo=obj[0],anno=year).aggregate(total=Sum('infraestructura__cantidad'))['total']
            if instalaciones == None:
                instalaciones = 0

            if obj[0] == 7 or obj[0] == 8:
                avg_capacidad = "---"
            else:
                avg_capacidad = filtro.filter(infraestructura__tipo=obj[0],anno=year).aggregate(total=Avg('infraestructura__capacidad'))['total']
                if avg_capacidad == None:
                    avg_capacidad = 0

            tabla_infraestructura.append([obj[1],int(instalaciones),avg_capacidad])

            #grafico estado de las intalaciones -----------------------------------------
            estado = {}
            for x in ESTADO_CHOICES:
                conteo = filtro.filter(infraestructura__tipo=obj[0],infraestructura__estado=x[0],anno=year).count()
                estado[x[1]] = saca_porcentajes(conteo,count_org,False)
            infraestructura[obj[1]] = estado

        #Cacao en baba acopiado en el último año-------------------------------------
        frec1,frec2,frec3,frec4,frec5 = 0,0,0,0,0

        cacao_baba = collections.OrderedDict()

        sum_cacao_baba = filtro.filter(anno=year).aggregate(area_total=Sum('comercializacion_org__cacao_baba_acopiado'))['area_total']
        avg_cacao_baba = filtro.filter(anno=year).aggregate(area_total=Avg('comercializacion_org__cacao_baba_acopiado'))['area_total']

        for obj in filtro.filter(anno=year).values_list('comercializacion_org__cacao_baba_acopiado', flat=True):
            if obj >= 1 and obj <= 1000:
                frec1 += 1
            if obj > 1000 and obj <= 2000:
                frec2 += 1
            if obj > 2000 and obj <= 3000:
                frec3 += 1
            if obj > 3000 and obj <= 4000:
                frec4 += 1
            if obj > 4000:
                frec5 += 1

        total_frecuencia_baba = frec1 + frec2 + frec3 + frec4 + frec5

        #cacao baba dic
        cacao_baba['1-1000 qq'] = (frec1,saca_porcentajes(frec1,total_frecuencia_baba,False))
        cacao_baba['1001-2000 qq'] = (frec2,saca_porcentajes(frec2,total_frecuencia_baba,False))
        cacao_baba['2001-3000 qq'] = (frec3,saca_porcentajes(frec3,total_frecuencia_baba,False))
        cacao_baba['3001-4000 qq'] = (frec4,saca_porcentajes(frec4,total_frecuencia_baba,False))
        cacao_baba['> 4000 qq'] = (frec5,saca_porcentajes(frec5,total_frecuencia_baba,False))

        #Cacao en seco comercializado el último año------------------------------------
        frec1,frec2,frec3,frec4,frec5 = 0,0,0,0,0

        cacao_seco = collections.OrderedDict()

        sum_cacao_seco = filtro.filter(anno=year).aggregate(area_total=Sum('comercializacion_org__cacao_seco_comercializado'))['area_total']
        avg_cacao_seco = filtro.filter(anno=year).aggregate(area_total=Avg('comercializacion_org__cacao_seco_comercializado'))['area_total']

        for obj in filtro.filter(anno=year).values_list('comercializacion_org__cacao_seco_comercializado', flat=True):
            if obj >= 1 and obj <= 1000:
                frec1 += 1
            if obj > 1000 and obj <= 2000:
                frec2 += 1
            if obj > 2000 and obj <= 3000:
                frec3 += 1
            if obj > 3000 and obj <= 4000:
                frec4 += 1
            if obj > 4000:
                frec5 += 1

        total_frecuencia_seco = frec1 + frec2 + frec3 + frec4 + frec5

        #cacao baba dic
        cacao_seco['1-1000 qq'] = (frec1,saca_porcentajes(frec1,total_frecuencia_seco,False))
        cacao_seco['1001-2000 qq'] = (frec2,saca_porcentajes(frec2,total_frecuencia_seco,False))
        cacao_seco['2001-3000 qq'] = (frec3,saca_porcentajes(frec3,total_frecuencia_seco,False))
        cacao_seco['3001-4000 qq'] = (frec4,saca_porcentajes(frec4,total_frecuencia_seco,False))
        cacao_seco['> 4000 qq'] = (frec5,saca_porcentajes(frec5,total_frecuencia_seco,False))

        #Socios que entregan cacao al acopio el último año-----------------------------

        #Pre-Socios que entregan cacao al acopio el último año-------------------------
        
        #Tipo de producto comercializado-----------------------------------------------
        tipo_producto = {}
        for obj in TIPO_PROD_CHOICES:
            if obj[0] != 3:
                count = filtro.filter(anno=year,comercializacion_org__tipo_producto=obj[0]).count()
                tipo_producto[obj[1]] = count 

        #Certificación utilizada para comercializar cacao -----------------------------

        #Destino de la producción de cacao---------------------------------------------

        #Acceso a financiamiento para el acopio y comercialización---------------------

        #diccionario de los años ------------------------------------------------------
        anno[year] = (status,org_by_status,graf_bar_status,graf_pie_status,aspectos_juridicos,tabla_aspectos_juridicos,
                        documentacion,tabla_documantacion,socias,socios,pre_socias,pre_socios,rangos_area,
                        total_frecuencia_rangos,avg_area,rangos_organico,total_frecuencia_organico,avg_area_organico,
                        rangos_convencional,total_frecuencia_convecional,avg_area_convencional,tabla_infraestructura,
                        infraestructura,avg_cacao_baba,cacao_baba,total_frecuencia_baba,avg_cacao_seco,cacao_seco,
                        total_frecuencia_seco,tipo_producto)
        #------------------------------------------------------------------------------- 
        
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