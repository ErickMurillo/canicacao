from django.conf.urls import patterns, include, url
from django.contrib import admin

#url monitoreo
urlpatterns = patterns('monitoreo.views',
  
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', 'IndexView', name='index'),
    url(r'^consulta', 'consulta', name='consulta'),
    url(r'^dashboard', 'dashboard', name='dashboard'),
    
    #indicadores
    url(r'^educacion', 'educacion', name='educacion'),
    url(r'^propiedad', 'propiedad', name='propiedad'),
    url(r'^uso-tierra', 'uso_tierra', name='uso-tierra'),
    url(r'^produccion', 'produccion', name='produccion'),
    url(r'^riesgos', 'riesgos', name='riesgos'),
    url(r'^comercializacion', 'comercializacion', name='comercializacion'),
    url(r'^genero', 'genero', name='genero'),
<<<<<<< HEAD
    url(r'^reforestacion', 'reforestacion', name='reforestacion'),
=======
    url(r'^caracterizacion', 'caracterizacion_terreno', name='caracterizacion-terreno'),
>>>>>>> carlos/master
    #mapa
    url(r'^mapa/$', 'obtener_lista', name='obtener-lista'),
    
    #filtros
    #url(r'^ajax/fechas/$', 'get_fecha', name='get_fecha'),
    url(r'^ajax/organi/$', 'get_organi', name='get-organi'),
    url(r'^ajax/munis/$', 'get_munis', name='get-munis'),
    url(r'^ajax/comunies/$', 'get_comunies', name='get-comunies'),
)

urlpatterns += patterns('',
    url(r'^xls/$', 'monitoreo.utils.save_as_xls'),
    )
#url organizacion
urlpatterns += patterns('organizacion.views',
    url(r'^org-mapa/$', 'obtener_lista_org', name='obtener-lista-org'),
    url(r'^organizacion', 'get_organizacion', name='organizacion'),
    url(r'^orgdetail', 'get_org_detail', name='orgdetail'),
)
