from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
#from .forms import *
import json as simplejson
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Sum, Count, Avg

# Create your views here.
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

def get_organizacion(request):
    
    return render(request, "organizacion/organizacion.html")

def get_org_detail(request):
    
    return render(request, "organizacion/orgdetail.html")