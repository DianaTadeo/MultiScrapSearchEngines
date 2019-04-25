#!/usr/bin/python
# -*- coding: utf-8 -*-

import busquedaPrueba as busqueda

import bs4
import re
import urllib

def beautifulSoup(query_search_engine, parser = 'lxml'):
	return 	bs4.BeautifulSoup(query_search_engine, parser)

def getLinks(lista):
	return filter(None, [ None if lista[i] is not None and (lista[i] is '#' or lista[i].startswith('/')) else lista[i] for i in range(0,len(lista)) ])

def getLinksFiletype(lista, search):
	operacion=re.match(r'(filetype):(.+)($| (.*))',search)
	print operacion.groups()
	filetype = operacion.group(2).split()[0]
	print filetype
	return [ lista[i] for i in range(0,len(lista)) if re.search(r'%s$' % filetype, lista[i]) ]

def printLinks(links):
	for link in links:
		print link

def getResults(search, links):
	if 'filetype' in search:
		printLinks(getLinksFiletype(links, search[search.find('filetype:'):]))
if __name__ == '__main__':
	search = 'filetype:pdf unam site:unam.mx'
	#search = 'ip:192.168'
	search_engines = ['Google', 'Bing', 'Baidu', 'Yahoo']
	#search_engines = ['DuckDuckGo']
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
			links_yahoo = [ urllib.unquote_plus(i)[i.find('http'):] for i in str(links).split('/') if i.startswith('RU') ]
			getResults(search,links_yahoo)
		elif search_engine == 'Baidu':
			links = getLinks([ href.find('a', href=True)['href'] for href in soup.findAll('div', {'class': 'c-container'}) ])  # baidu
			printLinks(links)
