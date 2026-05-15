from django import template
from django.apps import apps

register = template.Library()

@register.filter
def verbose_name(obj):
	return obj._meta.verbose_name

@register.filter
def verbose_name_plural(obj):
	return obj._meta.verbose_name_plural

@register.simple_tag
def get_model_verbose_name(app, model):
	return apps.get_model(app, model)._meta.verbose_name.title()

@register.simple_tag
def get_model_verbose_name_plural(app, model):
	return apps.get_model(app, model)._meta.verbose_name_plural.title()

@register.simple_tag
def get_field_model_verbose_name(app, model, field):
	return apps.get_model(app, model)._meta.get_field(field).verbose_name.title()

@register.simple_tag
def get_field_model_verbose_name_plural(app, model, field):
	return apps.get_model(app, model)._meta.get_field(field).verbose_name_plural.title()

@register.simple_tag
def get_app_verbose_name(app):
	return apps.get_app_config(app).verbose_name
