from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('monitoreo.views',
    # Examples:
    # url(r'^$', 'canicacao.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^$', 'IndexView', name='index'),
    url(r'^dashboard', 'dashboard', name='dashboard'),

    #filtros
    url(r'^ajax/organi/$', 'get_organi', name='get-organi'),
    url(r'^ajax/munis/$', 'get_munis', name='get-munis'),
    url(r'^ajax/comunies/$', 'get_comunies', name='get-comunies'),
)
