from setuptools import setup

setup(
	name = 'django-power-views',
	version = '1.3',
	packages = ['djangopowerviews'],
	description = 'View\'s extra para django que permiten busqueda sobre listas y redireccion con anclas',
	long_description = open('README.md', encoding='utf-8').read(),
	long_description_content_type = 'text/markdown',
	author = 'darkdeymon',
	author_email = 'darkdeymon04@gmail.com',
	url = 'https://github.com/DARKDEYMON/django-power-views',
	install_requires = [
		'django>=5.1'
	]
)
