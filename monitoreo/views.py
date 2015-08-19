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

def IndexView(request,template="monitoreo/index.html"):
    mujeres = Encuesta.objects.filter(persona__sexo='2').count()
    hombres = Encuesta.objects.filter(persona__sexo='1').count()
    area_cacao = Encuesta.objects.all().aggregate(area_cacao=Sum('area_cacao__area'))['area_cacao']
    produccion = Encuesta.objects.all().aggregate(total=Sum('produccion_cacao',
                                                            field="produccion_c_baba + produccion_c_seco + " +
                                                            "produccion_c_fermentado + produccion_c_organico"))['total']
    organizaciones = Organizacion.objects.all().count()

    return render(request, template, locals())

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


def dashboard(request,template='monitoreo/dashboard.html'):
    filtro = _queryset_filtrado(request)
    #nuevas salidas

    #conversiones###############
    hectarea = 0.7050
    tonelada = 0.1
    libra_tonelada = 0.00045359237
    ############################

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

    anno = collections.OrderedDict()

    for year in request.session['anno']:
        familias_year = filtro.filter(anno=year).count()
        #areas de cacao por edad de plantacion -----------------------------------------------------------------
        areas = {}
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
        area_prod = filtro.filter(anno=year).aggregate(area_cacao=Sum('plantacion__area'))['area_cacao']
        if area_prod == None:
            area_prod = 0

        baba = filtro.filter(anno=year).aggregate(cacao_baba_s=Sum('produccion_cacao__produccion_c_baba'))['cacao_baba_s']
        if baba == None:
            baba = 0

        seco = filtro.filter(anno=year).aggregate(cacao_seco_s=Sum('produccion_cacao__produccion_c_seco'))['cacao_seco_s']
        if seco == None:
            seco = 0

        fermentado = filtro.filter(anno=year).aggregate(cacao_fer_s=Sum('produccion_cacao__produccion_c_fermentado'))['cacao_fer_s']
        if fermentado == None:
            fermentado = 0

        organico = filtro.filter(anno=year).aggregate(cacao_org_s=Sum('produccion_cacao__produccion_c_organico'))['cacao_org_s']
        if organico == None:
            organico = 0

        area_hectarea = area_prod * float(hectarea)

        try:
            rendimiento_seco = ((baba/3) + seco) * 100 / area_hectarea
        except:
            rendimiento_seco = 0

        try:
            rendimiento_fer = (fermentado * 100) / area_hectarea

        except:
            rendimiento_fer = 0

        try:
            rendimiento_org = (organico * 100) / area_hectarea
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
        #auto-consumo vs venta
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

        comercializacion = {}

        for obj in PRODUCTO_CHOICES:
            if obj[0] == 3:
                try:
                    auto_consumo = ((filtro.filter(anno=year,comercializacion_cacao__producto=obj[0]).aggregate(total=Sum(
                                'comercializacion_cacao__auto_consumo'))['total'] )/ 3) * tonelada
                except:
                    auto_consumo = 0

                try:
                    venta = ((filtro.filter(anno=year,comercializacion_cacao__producto=obj[0]).aggregate(total=Sum(
                                'comercializacion_cacao__venta'))['total'])/ 3) * tonelada
                except:
                    venta = 0

            elif obj[0] == 4:
                try:
                    auto_consumo = (filtro.filter(anno=year,comercializacion_cacao__producto=obj[0]).aggregate(total=Sum(
                                'comercializacion_cacao__auto_consumo'))['total'] ) * tonelada
                except:
                    auto_consumo = 0

                try:
                    venta = (filtro.filter(anno=year,comercializacion_cacao__producto=obj[0]).aggregate(total=Sum(
                                'comercializacion_cacao__venta'))['total']) * tonelada
                except:
                    venta = 0
            else:
                try:
                    auto_consumo = (filtro.filter(anno=year,comercializacion_cacao__producto=obj[0]).aggregate(total=Sum(
                                'comercializacion_cacao__auto_consumo'))['total']) * libra_tonelada
                except:
                    auto_consumo = 0

                try:
                    venta = (filtro.filter(anno=year,comercializacion_cacao__producto=obj[0]).aggregate(total=Sum(
                                'comercializacion_cacao__venta'))['total'] ) * libra_tonelada
                except:
                    venta = 0

            comercializacion[obj[1]] = (auto_consumo,venta)

        #destino de produccion
        destino_dic = {}
        lista = []
        for x in Comercializacion_Cacao.objects.filter(encuesta__anno=year):
            if x.quien_vende != None:
                for y in x.quien_vende:
                    lista.append(int(y))

        list_count = len(lista)

        for obj in QUIEN_VENDE_CHOICES:
            p = lista.count(obj[0])
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
                        p_seco,p_fermentado,p_organico,avg_cacao,socio,no_socio,comercializacion,
                        prod_depto,destino_dic,destino_org_dic)


    return render(request, template, locals())

#nivel de educacion
def educacion(request,template='monitoreo/educacion.html'):
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

def propiedad(request,template='monitoreo/propiedad.html'):
    filtro = _queryset_filtrado(request)

    familias = filtro.count()

    count_si = filtro.filter(tenencia_propiedad__dueno_propiedad='1').count()

    count_no = filtro.filter(tenencia_propiedad__dueno_propiedad='2').count()

    dueno = saca_porcentajes(count_si,familias,False)
    no_dueno = saca_porcentajes(count_no,familias,False)

    dic2 = {}
    for x in Situacion.objects.all():
        objeto1 = filtro.filter(tenencia_propiedad__no=x).count()
        dic2[x] = saca_porcentajes(objeto1,count_no,False)
    
    dic = {}
    for e in PROPIEDAD_CHOICE:
        for x in e:
            objeto = filtro.filter(tenencia_propiedad__si=e[0]).count()
            dic[e[1]] = saca_porcentajes(objeto,count_si,False)
    print dic
    return render(request, template, locals())

def uso_tierra(request,template='monitoreo/uso_tierra.html'):
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

def produccion(request,template='monitoreo/produccion.html'):
    filtro = _queryset_filtrado(request)
    tonelada = 0.1

    baba = (filtro.aggregate(baba=Sum('produccion_cacao__produccion_c_baba'))['baba'] ) / 3
    seco = (filtro.aggregate(seco=Sum('produccion_cacao__produccion_c_seco'))['seco'] + baba ) * tonelada
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

    return render(request, template, locals())

def riesgos(request,template='monitoreo/riesgos.html'):
    filtro = _queryset_filtrado(request)
    familias = filtro.count()

    riesgos = {}
    riesgos_tabla = {}
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

    plantas = {}
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
    print mercados
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
                                saca_porcentajes(distribucion_cacao,familias,False),
                                saca_porcentajes(venta_cacao,familias,False),
                                saca_porcentajes(d_tecnologia_secado,familias,False),
                            )
    return render(request, template, locals())

def comercializacion(request,template='monitoreo/comercializacion.html'):
    filtro = _queryset_filtrado(request)
    familias = filtro.count()

    tabla_productos = []
    for obj in PRODUCTO_CHOICES:
        producto = filtro.filter(comercializacion_cacao__producto=obj[0]).aggregate(
                    auto_consumo=Avg('comercializacion_cacao__auto_consumo'),
                    venta=Avg('comercializacion_cacao__venta'),
                    precio_venta=Avg('comercializacion_cacao__precio_venta'))

        #validacion y formato float
        if producto['auto_consumo'] != None:
           auto_consumo = float("{0:.2f}".format(producto['auto_consumo']))
        else:
            auto_consumo = 0

        if producto['venta'] != None:
           venta = float("{0:.2f}".format(producto['venta']))
        else:
            venta = 0

        if producto['precio_venta'] != None:
           precio_venta = float("{0:.2f}".format(producto['precio_venta']))
        else:
            precio_venta = 0
        #-----------------------------------------------------------
        fila = [obj[1],auto_consumo,venta,precio_venta]

        tabla_productos.append(fila)
    distancia = filtro.aggregate(avg=Avg('distancia_comercio_cacao__distancia'))['avg']

    return render(request, template, locals())

def genero(request,template='monitoreo/genero.html'):
    filtro = _queryset_filtrado(request)

    genero = {}
    suma = 0
    for obj in Actividades_Produccion.objects.all():
        mujer = filtro.filter(genero__actividades=obj).count()
        genero[obj] = mujer

    #recibe ingrsos x actividades
    count_genero = Genero.objects.filter(encuesta=filtro).count()
    dic = {}
    for obj in SI_NO_CHOICES:
    	recibe_ing = filtro.filter(genero__ingresos=obj[0]).count()
    	dic[obj[1]] = saca_porcentajes(recibe_ing,count_genero,False)

    avg_ingresos = filtro.aggregate(avg=Avg('genero__ingreso_mesual'))['avg'] 

    destino_dic = {}
    for x in Destino_Ingresos.objects.all():
    	destino = filtro.filter(genero__destino_ingresos_2=x).count()
    	destino_dic[x] = destino
    	
    #---------------------------------------------------------------------
    decisiones = {}
    lista = []
    for obj in Genero.objects.filter(encuesta=filtro):
        if obj.decisiones != None:
            for x in obj.decisiones:
                lista.append(int(x))

    DECISIONES_CHOICES = (
	(1,'Siembra de cacao'),
	(2,'Cosecha de cacao'),
	(3,'Venta de cacao'),
	(4,'Ingresos de cacao'),
	)

    for dec in DECISIONES_CHOICES:
        p2 = lista.count(dec[0])
        decisiones[dec[1]] = p2

    return render(request, template, locals())

def reforestacion(request,template='monitoreo/reforestacion.html'):
	filtro = _queryset_filtrado(request)
	familias = filtro.count()

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

def organizacion_productiva(request,template='monitoreo/org_productiva.html'):
	filtro = _queryset_filtrado(request)

	servicio_dic = {}
	for obj in Tipos_Servicio.objects.all():
		servicio = filtro.filter(organizacion_asociada__tipos_servicio=obj).count()
		servicio_dic[obj] = servicio

	beneficio_dic = {}
	for x in Beneficios.objects.all():
		beneficio = filtro.filter(organizacion_asociada__beneficios=x).count()
		beneficio_dic[x] = beneficio

	return render(request, template, locals())

def capacitaciones(request,template='monitoreo/capacitaciones.html'):
    filtro = _queryset_filtrado(request)

    dic = {}
    for obj in CAPACITACIONES_CHOICES:
        lista = []
        capacitaciones = {}
        for cap in Capacitaciones_Tecnicas.objects.filter(encuesta=filtro,capacitaciones=obj[0]):
            for x in cap.opciones:
                lista.append(int(x))

        for xz in OPCIONES_CAPACITACIONES_CHOICES:
            p2 = lista.count(xz[0])
            capacitaciones[xz[1]] = p2
        dic[obj[1]] = capacitaciones


    capacitaciones_2 = {}
    lista = []
    for obj in Capacitaciones_Tecnicas.objects.filter(encuesta=filtro):
        for x in obj.opciones:
            lista.append(int(x))

    for obj_1 in OPCIONES_CAPACITACIONES_CHOICES:
        p2 = lista.count(obj_1[0])
        capacitaciones_2[obj_1[1]] = p2

    #socioeconomicas------------------------------------------------------------------------------
    dic_socio = {}
    for obj in CAPACITACIONES_SOCIO_CHOICES:
        lista_socio = []
        capacitaciones_socio = {}
        for cap_socio in Capacitaciones_Socioeconomicas.objects.filter(encuesta=filtro,capacitaciones_socio=obj[0]):
            if cap_socio.opciones_socio != None:
                for z in cap_socio.opciones_socio:
                    lista_socio.append(int(z))

        for xc in OPCIONES_CAPACITACIONES_CHOICES:
            p = lista_socio.count(xc[0])
            capacitaciones_socio[xc[1]] = p
        dic_socio[obj[1]] = capacitaciones_socio


    capacitaciones_socio = {}
    lista_1 = []
    for obj_socio in Capacitaciones_Socioeconomicas.objects.filter(encuesta=filtro):
        if obj_socio.opciones_socio != None:
            for x in obj_socio.opciones_socio:
                lista_1.append(int(x))

    for obj_1_socio in OPCIONES_CAPACITACIONES_CHOICES:
        p = lista_1.count(obj_1_socio[0])
        capacitaciones_socio[obj_1_socio[1]] = p

    return render(request, template, locals())

def capacitaciones_socio(request,template='monitoreo/capacitaciones_socio.html'):
	filtro = _queryset_filtrado(request)

	dic_socio = {}
	for obj in CAPACITACIONES_SOCIO_CHOICES:
		lista = []
		capacitaciones = {}
		for cap in Capacitaciones_Socioeconomicas.objects.filter(encuesta=filtro,capacitaciones_socio=obj[0]):
			if cap.opciones_socio != None:
				for x in cap.opciones_socio:
					lista.append(int(x))

		for xz in OPCIONES_CAPACITACIONES_CHOICES:
			p = lista.count(xz[0])
			capacitaciones[xz[1]] = p
		dic_socio[obj[1]] = capacitaciones


	capacitaciones_socio = {}
	lista_1 = []
	for obj in Capacitaciones_Socioeconomicas.objects.filter(encuesta=filtro):
		if obj.opciones_socio != None:
			for x in obj.opciones_socio:
				lista_1.append(int(x))

	for obj_1 in OPCIONES_CAPACITACIONES_CHOICES:
		p = lista_1.count(obj_1[0])
		capacitaciones_socio[obj_1[1]] = p

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


#SALIDAS CARLOS
def caracterizacion_terreno(request,template='monitoreo/caracterizacion_terreno.html'):
    filtro = _queryset_filtrado(request)
    familias = filtro.count()

    #caracteristicas del terrenos
    tabla_textura = {}
    for k in TEXTURA_CHOICES:
        query = filtro.filter(caracterizacion_terreno__textura_suelo = k[0])
        frecuencia = query.count()
        textura = filtro.filter(caracterizacion_terreno__textura_suelo=k[0]).aggregate(textura=Count('caracterizacion_terreno__textura_suelo'))['textura']
        por_textura = saca_porcentajes(textura, familias)
        tabla_textura[k[1]] = {'textura':textura,'por_textura':por_textura}

    #pendientes
    tabla_pendiente = {}
    for k in PENDIENTE_CHOICES:
        query = filtro.filter(caracterizacion_terreno__pendiente_terreno = k[0])
        frecuencia = query.count()
        pendiente = filtro.filter(caracterizacion_terreno__pendiente_terreno=k[0]).aggregate(pendiente=Count('caracterizacion_terreno__pendiente_terreno'))['pendiente']
        por_pendiente = saca_porcentajes(pendiente, familias)
        tabla_pendiente[k[1]] = {'pendiente':pendiente,'por_pendiente':por_pendiente}

    #pendientes
    tabla_hojarasca = {}
    for k in HOJARASCA_CHOICES:
        query = filtro.filter(caracterizacion_terreno__contenido_hojarasca = k[0])
        frecuencia = query.count()
        horajasca = filtro.filter(caracterizacion_terreno__contenido_hojarasca=k[0]).aggregate(horajasca=Count('caracterizacion_terreno__contenido_hojarasca'))['horajasca']
        por_horajasca = saca_porcentajes(horajasca, familias)
        tabla_hojarasca[k[1]] = {'horajasca':horajasca,'por_horajasca':por_horajasca}

    #Profundo
    tabla_profundidad = {}
    for k in PROFUNDIDAD_CHOICES:
        query = filtro.filter(caracterizacion_terreno__porfundidad_suelo = k[0])
        frecuencia = query.count()
        profundidad = filtro.filter(caracterizacion_terreno__porfundidad_suelo=k[0]).aggregate(profundidad=Count('caracterizacion_terreno__porfundidad_suelo'))['profundidad']
        por_profundidad = saca_porcentajes(profundidad, familias)
        tabla_profundidad[k[1]] = {'profundidad':profundidad,'por_profundidad':por_profundidad}

    tabla_drenaje = {}
    for k in DRENAJE_CHOICES:
        query = filtro.filter(caracterizacion_terreno__drenaje_suelo = k[0])
        frecuencia = query.count()
        drenaje = filtro.filter(caracterizacion_terreno__drenaje_suelo=k[0]).aggregate(drenaje=Count('caracterizacion_terreno__drenaje_suelo'))['drenaje']
        por_drenaje = saca_porcentajes(drenaje, familias)
        tabla_drenaje[k[1]] = {'drenaje':drenaje,'por_drenaje':por_drenaje}

    return render(request, template, locals())

def mitigacion_riesgos(request,template='monitoreo/mitigacion_riesgos.html'):
    filtro = _queryset_filtrado(request)
    familias = filtro.count()

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

def tipo_certificacion(request,template='monitoreo/tipo_certificacion.html'):
    filtro = _queryset_filtrado(request)
    familias = filtro.count()

    #caracteristicas del terrenos
    tabla_certificacion = {}
    for k in Lista_Certificaciones.objects.all():
        tipos = filtro.filter(certificacion__tipo = k).count()

        tabla_certificacion[k.nombre] = saca_porcentajes(tipos,familias,False)

    return render(request, template, locals())

def tecnicas_aplicadas(request,template='monitoreo/tecnicas_aplicadas.html'):
    filtro = _queryset_filtrado(request)
    familias = filtro.count()
   
    #VVEROS
    viveros = {}
    lista_viveros = []
    for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
        if obj.viveros != None:
            for x in obj.viveros:
                lista_viveros.append(int(x))
 
    for op in VIVEROS_CHOICES:
        p2 = lista_viveros.count(op[0])
        viveros[op[1]] = p2
    
    #FERTILIZACION_CHOICES
    fertilizacion = {}
    lista_fertilizacion = []
    for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
        if obj.fertilizacion != None :
            for x in obj.fertilizacion:
                lista_fertilizacion.append(int(x))

    for op in FERTILIZACION_CHOICES:
        p2 = lista_fertilizacion.count(op[0])
        fertilizacion[op[1]] = p2

    #pract_manejo_fis
    pract_manejo_fis = {}
    lista_pract_manejo_fis = []
    for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
        if obj.pract_manejo_fis != None:
            for x in obj.pract_manejo_fis:
                lista_pract_manejo_fis.append(int(x))

    for op in P_MANEJO_FIS_CHOICES:
        p2 = lista_pract_manejo_fis.count(op[0])
        pract_manejo_fis[op[1]] = p2

    #pract_manejo_prod
    pract_manejo_prod = {}
    lista_pract_manejo_prod = []
    for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
        if obj.pract_manejo_prod != None:
            for x in obj.pract_manejo_prod:
                lista_pract_manejo_prod.append(int(x))

    for op in P_MANEJO_PROD_CHOICES:
        p2 = lista_pract_manejo_prod.count(op[0])
        pract_manejo_prod[op[1]] = p2

    #pract_mejora_plat
    pract_mejora_plat = {}
    lista_pract_mejora_plat = []
    for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
        if obj.pract_mejora_plat != None:
            for x in obj.pract_mejora_plat:
                lista_pract_mejora_plat.append(int(x))

    for op in P_MEJORA_PLANT_CHOICES:
        p2 = lista_pract_mejora_plat.count(op[0])
        pract_mejora_plat[op[1]] = p2

    #pract_manejo_post_c
    pract_manejo_post_c = {}
    lista_pract_manejo_post_c = []
    for obj in Tecnicas_Aplicadas.objects.filter(encuesta=filtro):
        if obj.pract_manejo_post_c != None:
            for x in obj.pract_manejo_post_c:
                lista_pract_manejo_post_c.append(int(x))

    for op in P_MANEJO_POST_C_CHOICES:
        p2 = lista_pract_manejo_post_c.count(op[0])
        pract_manejo_post_c[op[1]] = p2
    
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

