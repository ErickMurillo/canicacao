from django.conf.urls import patterns, include, url
from django.contrib import admin

#url monitoreo
urlpatterns = patterns('monitoreo.views',
  
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', 'IndexView', name='index'),
    url(r'^consulta', 'consulta', name='consulta'),
    url(r'^dashboard', 'dashboard', name='dashboard'),
    url(r'^organizacion', 'get_organizacion', name='organizacion'),
    url(r'^orgdetail', 'get_org_detail', name='orgdetail'),
    
    #indicadores
    url(r'^educacion', 'educacion', name='educacion'),
    url(r'^propiedad', 'propiedad', name='propiedad'),
    url(r'^uso-tierra', 'uso_tierra', name='uso-tierra'),
    url(r'^produccion', 'produccion', name='produccion'),
    #mapa
    url(r'^mapa/$', 'obtener_lista', name='obtener-lista'),
    
    #filtros
    #url(r'^ajax/fechas/$', 'get_fecha', name='get_fecha'),
    url(r'^ajax/organi/$', 'get_organi', name='get-organi'),
    url(r'^ajax/munis/$', 'get_munis', name='get-munis'),
    url(r'^ajax/comunies/$', 'get_comunies', name='get-comunies'),
)

#url organizacion
urlpatterns += patterns('organizacion.views',
    url(r'^org-mapa/$', 'obtener_lista_org', name='obtener-lista-org'),
)
