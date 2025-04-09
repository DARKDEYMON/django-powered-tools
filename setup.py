from setuptools import setup

setup(
	name = 'django-powered-tools',
	version = '1.6',
	packages = ['djangopoweredtools'],
	description = 'View\'sv y herramientas extra para django que permiten busqueda sobre listas y redireccion con anclas y extras',
	long_description = open('README.md', encoding='utf-8').read(),
	long_description_content_type = 'text/markdown',
	author = 'darkdeymon',
	author_email = 'darkdeymon04@gmail.com',
	url = 'https://github.com/DARKDEYMON/django-powered-tools',
	install_requires = [
		'django>=5.1'
	]
)
