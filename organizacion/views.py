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

    dic = {}
    for obj in SI_NO_CHOICES:
        personeria_juridica = filtro.filter(aspectos_juridicos__tiene_p_juridica=obj[0]).count()
        act_perso_juridica = filtro.filter(aspectos_juridicos__act_p_juridica=obj[0]).count()
        solvencia_tributaria = filtro.filter(aspectos_juridicos__solvencia_tributaria=obj[0]).count()
        junta_directiva = filtro.filter(aspectos_juridicos__junta_directiva=obj[0]).count()
        socios = filtro.filter(aspectos_juridicos__lista_socios=obj[0]).count()

        lista = [personeria_juridica,act_perso_juridica,solvencia_tributaria,junta_directiva,socios]
        dic[obj[1]] = lista

    documentacion = {}
    for x in DOCUMENTOS_CHOICES:
        dic_result = {}
        for obj in SI_NO_CHOICES:
            result = filtro.filter(documentacion__documentos=x[0],documentacion__si_no=obj[0]).count()
            dic_result[obj[1]] = result
        documentacion[x] = dic_result

    print documentacion
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
