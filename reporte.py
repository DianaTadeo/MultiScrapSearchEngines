#!/usr/bin/python
# -*- coding: utf-8 -*-

import busqueda
from lxml import etree
from lxml import objectify
import os.path as path
import bs4
import re
from urllib import unquote_plus

def beautifulSoup(query_search_engine, parser = 'lxml'):
	"""Función que extrae el contenido de la petición que se realiza a los
	motores de búsqueda para poder obtener los resultados.
	Recibe: query_search_engine (resultado de la petición al motor)
			parser ( es el parser que se va a utilizar, por defecto es lxml)
	Devuelve: el contenido de la petición parseado
	"""
	return 	bs4.BeautifulSoup(query_search_engine, parser)

def getLinks(lista):
	"""Función que obtiene los enlaces de algunos motores de búsqueda excluyendo enlaces
	que son anuncios, cache, ayuda del motor o traducciones automáticas
	Recibe: lista (lista que sera analizada)
	Devuelve: lista con los enlaces finales
	"""
	# checar notLink -> []
	notLink = "^/|acl(ic|)k|translator|translate|fwlink|webcache|.*\.google|^[^https]|[&]q|3ds|exalead|askmediagroup|(about|help)\.ask"
	return list(set(filter(None, [ None if lista[i] is not None and (lista[i] is '#' or re.search(r'%s' % notLink, lista[i]) ) else lista[i] for i in range(0,len(lista)) ])))

def getLinksFiletype(lista, search):
	"""Función que obtiene los enlaces de los tipos de archivos buscados
	Recibe: lista (lista de enlaces a analizar)
			search (busqueda a realizar para obtener el tipo de archivo)
	Devuelve: lista de los enlaces a los archivos con el tipo de archivo buscado
	"""
	operacion=re.match(r'(filetype):(.+)($| (.*))',search)
	filetype = operacion.group(2).split()[0]
	return [ lista[i] for i in range(0,len(lista)) if re.search(r'%s$' % filetype, lista[i], re.I) ]

def getDomainAssociated(links,ip):
	### Se verifica que la ip no aparezca en la URL (para hacerlo más preciso sería consultar también el título del enlace)
	"""Función que obtiene los dominios asociados a la ip que se busca.
	Recibe: links (lista de los enlaces que se analiza)
			ip (string dirección ip para verificar que se obtiene el nombre de dominio y no alguna cosulta sobre dicha ip)
	Devuelve: lista con los dominios obtenidos
	"""
	return list(set([ links[i][links[i].find('//')+2:links[i].find('/',links[i].find('//')+2)] for i in range(0,len(links)) if not re.search(r'%s' % ip.split(':')[1], links[i]) ]))

def getMailAccounts(texts, domain):
	"""Función que obtiene las cuentas de correo asociadas al dominio que se busca. Si el dominio no se especifica,
		se devolverán todos los correos
	Recibe: texts (lista del contenido de cada enlace de la que se obtienen los correos)
			domain (string que indica el dominio del que se buscan las cuentas de correo)
	Devuelve: lista con los correos obtenidos
	"""
	domain_search = '[a-zA-Z.]+' if domain.split(':')[1] is '' else domain.split(':')[1].split(' ')[0]
	return list(set([ re.search(r'[a-zA-z._0-9]+[^_.]@%s' % domain_search,mail_account).group(0) for text in texts for mail_account in text.split() if re.match(r'.+@%s' % domain_search, mail_account) ]))

def returnLinks(links, search_engine = '', param = False):
	"""Función que devuelve las URL con los parámetros GET de acuerdo al valor de param (True o False).
	Recibe: links (lists de enlaces), param (bool que indica si se incluyen o no)
	Devuelve: lista con parametros o sin parámetros GET
	"""
	if not param and search_engine is not 'Baidu':	links = list(set([ link[:link.rfind('?')] if re.search(r'/.*\?', link) else link for link in links ]))
	return links

def printLinks(links):
	"""Función que muestra los enlaces obtenidos en la salida estándar."""
	for link in links:
		print link

def getResults(search, links, search_engine, param):
	"""Función que devuelve la lista de los resultados obtenidos de acuerdo a la búsquda realizada.
	Recibe: search (string de la búsqueda que se realiza), links (lista con los enlaces o texto obtenido del query),
			search_engine (motor de búsqueda para saber si se pueden obtener los resultados de él y el manejo de resultados),
			param (bool que indica si se muestran los parámetros GET)
	Devuelve: lista con los enlaces, dominios o correos de acuerdo a search"""
	if 'filetype:' in search:
		if search_engine == 'Baidu':	return returnLinks(links, search_engine, param)
		else:	return returnLinks(getLinksFiletype(links, search[search.find('filetype:'):]), param)
	elif 'ip:' in search:
		if search_engine in ['Bing', 'DuckDuckGo', 'Yahoo', 'AOL']:
			return getDomainAssociated(links, search[search.find('ip:'):])
	elif 'mail:' in search:
		return getMailAccounts(links, search[search.find('mail:'):])
	else:
		return returnLinks(links, search_engine, param)

def busquedaReporte(search, query, search_engine, param, formato):
	"""Función que realiza la busqueda de los enlaces, correos, domions asociados,
	de acuerdo  a la búsqueda que se realiza en cada uno de los motores de búsqueda.
	Recibe: search (búsqueda que se realiza)
			query (petición realizada al motor de búsqueda correspondiente)
			search_engine (motor de búsqueda sobre el que se realiza la misma)
			param (bool  que indica si se devuelven los parámetros GET)
	Devuelve: lista con los resultados
	"""
	soup = beautifulSoup(query)
	if search_engine in ['Google', 'Bing', 'DuckDuckGo', 'Exalead']:
		if 'mail:' in search:
			if search_engine == 'Google':	links = list(set([ href.text for href in soup.find_all('span', class_="st") ]))
			if search_engine == 'Bing':	links = list(set([ re.sub('\n\s*', '', href.find('p').text) for href in soup.find_all('div', class_="b_caption") ]))
			if search_engine == 'DuckDuckGo':	links = list(set([ href.text for href in soup.find_all('a', class_="result__snippet") ]))
			if search_engine == 'Exalead':	links = list(set([ href.text for href in soup.find_all('span', class_="ellipsis") ]))
		else:
			links = getLinks([ href.get('href') for href in soup.findAll('a') ]) # Google
	elif search_engine == 'Ask':
		if 'mail:' in search:	links = list(set([ re.sub('\n\s*', '', href.text) for href in soup.find_all('p', class_="PartialSearchResults-item-abstract") ]))
		else:	links = list(set([ href.get('href') for href in soup.find_all('a', class_="PartialSearchResults-item-title-link result-link") ]))

	elif search_engine in ['Yahoo', 'AOL']:
		if 'filetype:' in search or 'site:' in search: links_format = [ href.find('a', href=True)['href'] for href in soup.find('div', id='web').findAll('h3') ]  # filetype
		elif 'mail:' in search:	links = list(set([ href.text for href in soup.find_all('p', class_="lh-16") ]))
		else: links_format = [ href.get('href') for href in soup.find('div', id='results').findAll('a') if not re.search(r'acl(ic|)k|policies.oath', str(href)) ]
		if not 'mail' in search:	links = list(set([ unquote_plus(i)[i.find('http'):] for i in str(links_format).split('/') if i.startswith('RU') ]))

	elif search_engine == 'Baidu':
		if 'mail:' in search: links = [ href.text for href in soup.findAll('div', {'class': 'c-abstract'}) ]
		else:	links = getLinks([ href.find('a')['href'] for href in soup.findAll('div', {'class': 'c-container'}) ])  # baidu
	elif search_engine == 'Lycos':
		if 'mail:' in search: links = list(set([ href.text for href in soup.find_all('span', class_="result-description") ]))
		else:
			links_format = list(set([ href.get('href') for href in soup.find('div', {'class':'results search-results'}).findAll('a') ]))
			links = [ unquote_plus(i[i.find('http'):i.find('\'')]) for i in str(links_format).split('&') if i.startswith('as=') ]

	elif search_engine == 'Ecosia':
		if 'mail:' in search: links = list(set([ href.text for href in soup.find_all('p', class_="result-snippet") ]))
		else:	links = list(set([ href.get('href') for href in soup.find_all('a', class_="result-url js-result-url") ]))
	else:
		print soup.prettify('utf-8')
		exit(1)
	listaResultados = getResults(search, links, search_engine, param)
	if formato:
		resultados = getResults(search, links, search_engine, param) # getResults devuelve la lista de los enlaces, correos, dominios encontrados
		if formato.upper()=='XML':
			make_FormatXML(resultados, search_engine, search)
		elif formato.upper()=='HTML':
			make_FormatHTML(resultados, search_engine, search)
		elif formato.upper()=='TXT':
			make_FormatTXT(resultados, search_engine, search)
	else:
		printLinks(getResults(search, links, search_engine, param))

def make_FormatXML(resultados, search_engine, search):
	"""
	Funcion que devuelve el reporte en un archivo XML
	si la bandera --format se encuentra activada.

	resultados: Lista de resultados obtenidos de la busqueda.
	search_engine: El buscador que se utilizo para la busqueda.
	search: La busqueda realizada
	"""
	if path.exists('Busquedas.xml'):
		#Si el archivo ya existe se obtiene la raiz, en este caso "data"
		tree = objectify.parse('Busquedas.xml')
		root = tree.getroot() #<data>
		el	= root.find('main') #Se busca el elemento que contiene las busquedas <main>
		result_search = etree.SubElement(el,'busqueda', name=''+search)
		engine = etree.SubElement(result_search, search_engine)
		#Guardamos los nuevos resultados
		for res in resultados:
			result = etree.SubElement(engine, 'resultado', res=res.decode('utf-8').strip())
		outFile = open('Busquedas.xml', 'w')
		tree.write(outFile)
	else:
		root = etree.Element('data')# se crea la raiz <data>
		doc = etree.ElementTree(root)
		el = etree.SubElement(root,'main') #se a;ade a la raiz el elemento <main>
		result_search=etree.SubElement(el, 'busqueda', name=search) #se agrega el elemento <busqueda>
		engine = etree.SubElement(result_search, search_engine) #Se agega el elemento de etiqueta searc_engine
		#Guardamos los resultados
		for res in resultados:
			result = etree.SubElement(engine, 'resultado', res=res.decode('utf-8').strip())
		outFile = open('Busquedas.xml', 'w')
		doc.write(outFile)

def make_FormatHTML(resultados, search_engine, search):
	"""
	Funcion que devuelve el reporte en un archivo HTML
	si la bandera --format se encuentra activada.

	resultados: Lista de resultados obtenidos de la busqueda.
	search_engine: El buscador que se utilizo para la busqueda.
	search: La busqueda realizada
	"""
	if path.exists('Busquedas.html'):
		tree = objectify.parse('Busquedas.html')
		root = tree.getroot()
		body_doc = root.find('body')
		h2 = objectify.SubElement(body_doc, 'h2')
		h2._setText('Busqueda: "'+ search+'"')
		div = etree.SubElement(body_doc, 'div')
		h3 = objectify.SubElement(div, 'h3')
		h3._setText(''+search_engine)
		for res in resultados:
			result = objectify.SubElement(div, 'a', href=res)
			result._setText(res.decode('utf-8'))
			br = etree.SubElement(div, 'br')
		with open('Busquedas.html', 'w') as archivo:
			tree.write(archivo)
	else:
		root = etree.Element('html')
		doc = etree.ElementTree(root)
		head_doc = etree.SubElement(root,'head')
		title = etree.SubElement(head_doc,'title')
		title.text = "Reporte de Busquedas"
		body_doc = etree.SubElement(root,'body')
		h1 =etree.SubElement(body_doc, 'h1')
		h1.text = 'Reporte de Busquedas'
		h2 = etree.SubElement(body_doc, 'h2')
		h2.text = 'Busqueda: "'+ search+'"'
		div = etree.SubElement(body_doc, 'h2')
		h3 = etree.SubElement(div, 'h3')
		h3.text = ''+search_engine
		for res in resultados:
			result = etree.SubElement(div, 'a', href=res)
			result.text = res.decode('utf-8')
			br = etree.SubElement(div, 'br')
		with open('Busquedas.html', 'w') as archivo:
			doc.write(archivo)

def make_FormatTXT(resultados, search_engine, search):
	"""
	Funcion que devuelve el reporte en un archivo XML
	si la bandera --format se encuentra activada.

	resultados: Lista de resultados obtenidos de la busqueda.
	search_engine: El buscador que se utilizo para la busqueda.
	search: La busqueda realizada
	"""
	with open('Busquedas.txt', 'a') as archivo:
		archivo.write('\n--------------BUSQUEDA: "'+search+'"----------------\n')
		archivo.write('\n\tWEB SEARCH: '+search_engine+'\n')
		for res in resultados:
			archivo.write(res+'\n')
		archivo.close()
