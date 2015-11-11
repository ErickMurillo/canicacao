from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

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
    url(r'^reforestacion', 'reforestacion', name='reforestacion'),
    url(r'^caracterizacion', 'caracterizacion_terreno', name='caracterizacion-terreno'),
    url(r'^organizacion-productiva', 'organizacion_productiva', name='organizacion-productiva'),
    url(r'^capacitaciones', 'capacitaciones', name='capacitaciones'),
    url(r'^capacitaciones-socio', 'capacitaciones_socio', name='capacitaciones-socio'),
    url(r'^mitigacion', 'mitigacion_riesgos', name='mitigacion-riesgos'),
    url(r'^certificacion', 'tipo_certificacion', name='tipo-certificacion'),
    url(r'^tecnicas', 'tecnicas_aplicadas', name='tipo-tecnicas-aplicadas'),
    url(r'^ampliar-areas-cacao', 'ampliar_areas_cacao', name='ampliar-areas-cacao'),

    #mapa
    url(r'^mapa/$', 'obtener_lista', name='obtener-lista'),

    #filtros
    url(r'^ajax/organi/$', 'get_organi', name='get-organi'),
    url(r'^ajax/munis/$', 'get_munis', name='get-munis'),
    url(r'^ajax/comunies/$', 'get_comunies', name='get-comunies'),
)

urlpatterns += patterns('',
    url(r'^xls/$', 'monitoreo.utils.save_as_xls'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    )

#url organizacion
urlpatterns += patterns('organizacion.views',
    
    url(r'^org-mapa/$', 'obtener_lista_org', name='obtener-lista-org'),
    url(r'^organizacion/', 'get_organizacion', name='organizacion'),
    url(r'^org-dashboard/', 'orgdashboard', name='orgdashboard'),
    url(r'^status/', 'status', name='status'),
    url(r'^documentacion/', 'documentacion', name='documentacion'),
    url(r'^datos-productivos/', 'datos_productivos', name='datos-productivos'),
    url(r'^infraestructura/', 'infraestructura', name='infraestructura'),
    url(r'^detalle-org/(?P<id>[0-9]+)/$', 'get_org_detail', name='detail-org'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
