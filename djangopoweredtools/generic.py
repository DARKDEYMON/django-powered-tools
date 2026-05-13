from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.db.models import CharField
from django.db.models.functions import Cast
from operator import attrgetter
from django.urls import reverse_lazy
from djangopoweredtools.forms import *
from djangopoweredtools.constants import ID_OBJECT_TO_FIND

__all__ = [
	'ListSearchView',
	'FormPageRedirectView',
	'ModelExtraView',
	'CreateViewInternal',
	'UpdateViewInternal',
	'DeleteViewInternal'
]

class ListSearchView(ListView):
	"""
	Modelo de lista con formulario de busqueda y redireccion a objeto dentro la lista
	form_class:		si existe un formulario de búsqueda personalizado se renderiza como form el dato es forzoso
	fields_search:	es un dato forzosos de existir indica las filas sobre las que se buscar acepta relaciones
	ordering:		ordering es requerido
	"""

	form_class = SearchForm
	fields_search = []
	field_form_search_name = 'search'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = self.form_class(self.request.GET or None)
		return context

	@property
	def search(self):
		if not hasattr(self, '_search'):
			form = self.form_class(self.request.GET or None)

			if form.is_valid():
				self._search = form.cleaned_data.get(self.field_form_search_name)
			else:
				self._search = None

		return self._search

	def search_fields(self, query):
		search = self.search
		if (search and len(self.fields_search)!=0):
			trigram = None
			for field in self.fields_search:
				#self.model._meta.get_field(field)
				expr = TrigramSimilarity(Coalesce(Cast(field, CharField()), Value('')),search)
				trigram = expr if trigram is None else trigram + expr
			return query.annotate(
				similarity = trigram
			).order_by('-similarity')
		else:
			return query

	def get_queryset(self):
		query = super().get_queryset()
		return self.search_fields(query)

	def get(self, *args, **kwargs):
		redirect = self.redirect_to_object() 
		return redirect if redirect else super().get(*args, **kwargs)

	def redirect_to_object(self):
		if self.request.method == 'GET':
			if( ID_OBJECT_TO_FIND in self.request.GET and hasattr(self, 'paginate_by')):
				idobject = int(self.request.GET[ID_OBJECT_TO_FIND])
				query_ids = list(self.get_queryset().values_list('id', flat=True))
				page = query_ids.index(idobject) // self.get_paginate_by(self.get_queryset()) + 1
				return HttpResponseRedirect(f'{self.request.path}?page={page}#{idobject}')

class FormPageRedirectView(FormView):
	"""
	Modelo extra para usarse con ListSerachView para redirigir ala pagina del objeto deseado y este se redirija con un ancla
	"""
	def get_success_url(self):
		add =  f'?{ID_OBJECT_TO_FIND}={self.object.id}'
		return super().get_success_url() + add

class ModelExtraView(FormMixin):
	# model_extra:	se requiere pasar el modelo de relación este se renderisara por el pk pasado al view
	def get_context_data(self, *args , **kwargs):
		context = super().get_context_data(*args, **kwargs)
		if 'object_extra' not in context and hasattr(self, 'model_extra'):
			context['object_extra'] = self.model_extra.objects.get(id=self.kwargs['pk'])
		return context

class CreateViewInternal(CreateView, ModelExtraView):
	"""
	Modelo de guardado de vistas interna funciona con un model_extra o un ModelExtraView
	model_extra :	es requerido indica el modelo de relación con el que obtener la llave foránea 'estos modelos solo sirven en modelos
					que requieren un fk por ahora solo funciona si la llave foránea tiene por nombre en el modelo relacionado el mismo nombre
					en minúscula
	location: 		es requerido indica el lugar de donde sacar el pk para la redireccion
	"""
	def get_success_url(self):
		retriever = attrgetter(self.location)
		return reverse_lazy(self.success_url,kwargs={'pk':retriever(self.object)})
	def form_valid(self, form):
		setattr(form.instance, self.model_extra.__name__.lower(), self.get_context_data()['object_extra'])
		return super().form_valid(form)

class UpdateViewInternal(UpdateView):
	"""
	Modelo de guardado de vistas interna
	location: 		es requerido indica el lugar de donde sacar el pk para la redireccion
	"""
	def get_success_url(self):
		retriever = attrgetter(self.location)
		return reverse_lazy(self.success_url,kwargs={'pk':retriever(self.object)})

class DeleteViewInternal(DeleteView):
	"""
	Modelo de guardado de vistas interna
	location: 		es requerido indica el lugar de donde sacar el pk para la redireccion
	"""
	def get_success_url(self):
		retriever = attrgetter(self.location)
		return reverse_lazy(self.success_url,kwargs={'pk':retriever(self.object)})
