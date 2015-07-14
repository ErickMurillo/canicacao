from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from .forms import *

# Create your views here.
def _queryset_filtrado(request):
	params = {}
	if 'anno' in request.session:
		params['anno'] = request.session['anno']

	if request.session['departamento']:
		if not request.session['municipio']:
			municipios = Municipio.objects.filter(departamento__in=request.session['departamento'])
			params['persona__comunidad__municipio__in'] = municipios
		else:
			if request.session['comunidad']:
				params['persona__comunidad__in'] = request.session['comunidad']
			else:
				params['persona__comunidad__municipio__in'] = request.session['municipio']

	if requ.session['organizacion']:
		params['organizacion'] = request.session['organizacion']

	if requ.session['socio']:
		params['organizacion_asociada__socio'] = request.session['socio']


	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	return Encuesta.objects.filter(**params)

def IndexView(request,template="index.html"):
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

