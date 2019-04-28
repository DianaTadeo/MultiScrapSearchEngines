#!/usr/bin/python
# -*- coding: utf-8 -*-

import busquedaPrueba as busqueda

import bs4
import re
from urllib import unquote_plus

def beautifulSoup(query_search_engine, parser = 'lxml'):
	return 	bs4.BeautifulSoup(query_search_engine, parser)

def getLinks(lista):
	notLink = "^/|acl(ic|)k|translator|translate|fwlink|webcache|.*\.google|^[^https]|[&|?]q|3ds|exalead|askmediagroup|(about|help)\.ask"
	return list(set(filter(None, [ None if lista[i] is not None and (lista[i] is '#' or re.search(r'%s' % notLink, lista[i]) ) else lista[i] for i in range(0,len(lista)) ])))

def getLinksFiletype(lista, search):
	operacion=re.match(r'(filetype):(.+)($| (.*))',search)
	filetype = operacion.group(2).split()[0]
	print operacion.groups()
	print filetype
	return [ lista[i] for i in range(0,len(lista)) if re.search(r'%s$' % filetype, lista[i]) ]

def getDomainAssociated(links,ip):
	### Se verifica que la ip no aparezca en la URL (para hacerlo más preciso sería consultar también el título del enlace)
	return list(set([ links[i][links[i].find('//')+2:links[i].find('/',links[i].find('//')+2)] for i in range(0,len(links)) if not re.search(r'%s' % ip.split(':')[1], links[i]) ]))

def printLinks(links):
	for link in links:
		print link

def getResults(search, links, search_engine = ''):
	if 'filetype:' in search:
		if search_engine == 'Baidu':	printLinks(links)
		else:	printLinks(getLinksFiletype(links, search[search.find('filetype:'):]))
	elif 'ip:' in search:
		if search_engine in ['Bing', 'DuckDuckGo', 'Yahoo', 'AOL']:
			printLinks(getDomainAssociated(links, search[search.find('ip:'):]))
	else:
		printLinks(links)

def busquedaReporte(search, query, search_engine):
	#query = busqueda.search_results(search, search_engine, 50)[1]
	soup = beautifulSoup(query)
	if search_engine in ['Google', 'Bing', 'DuckDuckGo', 'Ask', 'Exalead']:
		links = getLinks([ href.get('href') for href in soup.findAll('a') ]) # Google
	elif search_engine in ['Yahoo', 'AOL']:
		if 'filetype:' in search or 'site:' in search: links_format = [ href.find('a', href=True)['href'] for href in soup.find('div', id='web').findAll('h3') ]  # filetype
		else: links_format = [ href.get('href') for href in soup.find('div', id='results').findAll('a') if not re.search(r'acl(ic|)k|policies.oath', str(href)) ]
		links = list(set([ unquote_plus(i)[i.find('http'):] for i in str(links_format).split('/') if i.startswith('RU') ]))
	elif search_engine == 'Baidu':
		links = getLinks([ href.find('a', href=True)['href'] for href in soup.findAll('div', {'class': 'c-container'}) ])  # baidu
	elif search_engine == 'Lycos':
		links_format = list(set([ href.get('href') for href in soup.find('div', {'class':'results search-results'}).findAll('a') ]))
		links = [ unquote_plus(i[i.find('http'):i.find('\'')]) for i in str(links_format).split('&') if i.startswith('as=') ]
	elif search_engine == 'Ecosia':
		links = list(set([ href.get('href') for href in soup.find_all('a', class_="result-url js-result-url") ]))
	else:
		print soup.prettify('utf-8')
		exit(1)
	getResults(search, links, search_engine)

if __name__ == '__main__':
	search = 'filetype:pdf unam site:unam.mx'
	#search = 'ip:192.168'
	#search_engines = ['Google', 'Bing', 'Baidu', 'Yahoo']
	search_engines = ['Gigablast']
	for search_engine in search_engines:
		query = busqueda.search_results(search, search_engine, 50)[1]
		soup = beautifulSoup(query)
		print search_engine
		#print soup
		if search_engine in ['Google', 'Bing']:
			links = getLinks([ href.get('href') for href in soup.findAll('a') ]) # Google
			getResults(search, links)
		elif search_engine == 'Yahoo':
			links = [ href.find('a', href=True)['href'] for href in soup.find('div', id='web').findAll('h3') ]
			links_yahoo = [ unquote_plus(i)[i.find('http'):] for i in str(links).split('/') if i.startswith('RU') ]
			getResults(search,links_yahoo)
		elif search_engine == 'Baidu':
			links = getLinks([ href.find('a', href=True)['href'] for href in soup.findAll('div', {'class': 'c-container'}) ])  # baidu
			printLinks(links)
