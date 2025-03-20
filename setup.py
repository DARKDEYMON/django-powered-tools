from setuptools import setup

setup(
	name = 'django-power-tools',
	version = '1.5',
	packages = ['djangopowertools'],
	description = 'View\'s extra para django que permiten busqueda sobre listas y redireccion con anclas',
	long_description = open('README.md', encoding='utf-8').read(),
	long_description_content_type = 'text/markdown',
	author = 'darkdeymon',
	author_email = 'darkdeymon04@gmail.com',
	url = 'https://github.com/DARKDEYMON/django-power-tools',
	install_requires = [
		'django>=5.1'
	]
)
