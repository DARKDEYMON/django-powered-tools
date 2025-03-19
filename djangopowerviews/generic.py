from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.db.models import CharField
from django.db.models.functions import Cast

class ListSearchView(FormMixin, ListView):
	"""
	form_class:		si existe un formulario de busqueda personalisado se renderiza como form
	fields_search:	es un dato forsosos de existir
	ordering:		ordering es requerido
	"""
	def get_success_url(self):
		return self.request.path

	def get_form(self, form_class=None):
		if form_class is None:
			form_class = self.get_form_class()
		if self.request.GET:
			return form_class(self.request.GET)
		else:
			return form_class(**self.get_form_kwargs())

	def get(self, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			self.search = form.cleaned_data['search'] if form.cleaned_data['search'] != '' else None
		redirect = self.redirect_to_object()
		return redirect if redirect else super().get(*args, **kwargs)

	def get_queryset(self):
		query = super().get_queryset()
		return self.search_fields(query)

	def search_fields(self, query):
		search = getattr(self,'search', None)
		if (search and len(self.fields_search)!=0):
			trigram = None
			for field in self.fields_search:
				#self.model._meta.get_field(field)
				if trigram==None:
					trigram = TrigramSimilarity(Coalesce(Cast(field, CharField()), Value('')),search)
				else:
					trigram = trigram + TrigramSimilarity(Coalesce(Cast(field, CharField()),Value('')),search)
			return query.annotate(
				similarity = trigram
			).order_by('-similarity')
		else:
			return query

	def redirect_to_object(self):
		if self.request.method == 'GET':
			if('idobject' in self.request.GET and hasattr(self, 'paginate_by')):
				idobject = int(self.request.GET['idobject'])
				query_ids = list(self.get_queryset().values_list('id', flat=True))
				page = query_ids.index(idobject) // self.get_paginate_by(self.get_queryset()) + 1
				return HttpResponseRedirect(self.request.path + '?page=' + str(page) + '#' + str(idobject))

class FormPageRedirectView(FormView):
	"""
	Modelo extra para usarse con ListSerachView para redirigir ala pagina del objeto deseado y este se redirija con un ancla
	"""
	def get_success_url(self):
		add =  '?idpage=' + str(self.object.id)
		return super().get_success_url() + add

class ModelExtraView(FormView):
	# model_extra:	se requiere pasar el modelo de relación este se renderisara por el pk pasado al view
	def get_context_data(self, *args , **kwargs):
		context = super().get_context_data(*args, **kwargs)
		if 'object_extra' not in context and hasattr(self, 'model_extra'):
			context['object_extra'] = self.model_extra.objects.get(id=self.kwargs['pk'])
		return context
