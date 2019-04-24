#!/usr/bin/python
# -*- coding: utf-8 -*-

import busquedaPrueba as busqueda

import bs4
import re

def beautifulSoup(query_search_engine):
	return 	bs4.BeautifulSoup(query_search_engine, 'lxml')

def getLinks(lista):
	return filter(None, [ None if lista[i] is not None and (lista[i] is '#' or lista[i].startswith('/')) else lista[i] for i in range(0,len(lista)) ])

def getLinksFiletype(lista, filetype):
	return filter(None, [ lista[i] if re.search(r'%s$' % filetype, lista[i]) else None for i in range(0,len(lista)) ])

def printLinks(links):
	for link in links:
		print link

if __name__ == '__main__':
	search = 'filetype:pdf unam site:unam.mx'
	### Por ahora solamente probado con Google
	keyword_google, query_google = busqueda.search_results(search, 'Google', 50)
	soup_google = beautifulSoup(query_google)
	#print soup_google.prettify().encode('utf-8')  # se formatea en html para poder obtener lo que se requiera con soup
	links_google = getLinks([ href.get('href') for href in soup_google.findAll('a') ])
	#printLinks(links_google)  # obtiene todos los enlaces encontrados de la consulta
	if 'filetype' in search:
		filetype = search[search.find('filetype:')+9:search.find(' ',search.find('filetype:'))]
		printLinks(getLinksFiletype(links_google, filetype))
