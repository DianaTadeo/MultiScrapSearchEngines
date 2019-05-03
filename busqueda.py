#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

def fetch_results(search_term, search_engine, number_results = 50, language_code = 'en'):
	"""Función que obtiene el resultado de la url correspondiente a cada motor de búsqueda con los términos a buscar.
	Recibe: search_term (términos de búsqueda), searc_engine (motor de búsqueda), number_results (número de resultados a buscar),
			language_code (idioma en el que se realizará la búsqueda)
	Devuelve: url (url con el formato de cada motor de búsqueda)
	"""
	assert isinstance(search_term, str), 'Search term must be a string'
	assert isinstance(number_results, int), 'Number of results must be an integer'
	escaped_search_term = search_term.replace(' ', '+')
	#url a la que se hara el request... en el primer {} va a ir el query
	####### Para cada motor de busqueda se formatea su url para hacer el get
	if search_engine == 'Google': url = 'https://www.google.com/search?q={}&num={}'.format(search_term, number_results)
	elif search_engine == 'DuckDuckGo': url = 'https://www.duckduckgo.com/html/?q={}'.format(search_term)
	elif search_engine == 'Bing': url = 'https://www.bing.com/search?q={}&count={}'.format(search_term, number_results)
	elif search_engine == 'Yahoo': url = 'https://search.yahoo.com/search?p={}&n={}'.format(search_term, number_results)
	elif search_engine == 'Baidu': url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd={}&rqlang=all&rsv_enter=1&rn={}'.format(search_term, number_results)
	elif search_engine == 'Ask': url = 'https://www.ask.com/web?q={}&page={}'.format(search_term, number_results)
	elif search_engine == 'AOL': url = 'https://search.aol.com/aol/search?q={}&b={}1&pz=10'.format(search_term,number_results)
	elif search_engine == 'Lycos': url = 'http://search.lycos.es/web/?q={}&OrigLycosTld=es&keyvol=1'.format(search_term)
	elif search_engine == 'Ecosia': url = 'https://www.ecosia.org/search?p={}&q={}'.format(number_results, search_term)
	elif search_engine == 'Exalead': url = 'https://www.exalead.com/search/web/results/?q={}&elements_per_page=10&start_index={}0'.format(search_term,number_results)

	return url

def findAO(search,op):
	"""
	Funcion que busca un operador binario y regresa su lado
	izquierdo y derecho

	search: cadena donde buscara el operador
	op: operador que sera buscado
	"""
	opAO_exist=re.search(op,search)
	if opAO_exist:
		return search[0:opAO_exist.start()].strip() , search[opAO_exist.start()+3:].strip()
	else:
		return "NO", "NO"



def buildQuery(search, web_search):
	"""
	Funcion que se encarga de construir el query a traves de una
	busqueda y de acuerdo al buscador.

	search: entrada de la busqueda
	web_search: buscador para el que se creara el query
	"""
	query=''
	res_AndL,res_AndR= findAO(search,'AND') #Revisa si hay AND's
	res_OrL, res_OrR= findAO(search,'OR') #Revisa si hay OR's
	if res_AndL!='NO': #Si hay AND se llama recursivamente buildQuery para el lado derecho y el izquierdo
		query+=op_and(buildQuery(res_AndL,web_search),buildQuery(res_AndR,web_search),web_search)
	elif res_OrL!='NO':#Si hay OR se llama recursivamente buildQuery para el lado derecho y el izquierdo
		query+=op_or(buildQuery(res_OrL,web_search),buildQuery(res_OrR,web_search),web_search)
	else: #Si no hay ni AND ni OR prosigue revisando operadores
		if search == 'mail:':
			if web_search in ['Yahoo', 'Ecosia']:	search += 'mail.com'
			elif web_search == 'DuckDuckGo': search += '\"yahoo.com\" or \"hotmail.com\" or \"gmail.com\"'
			elif web_search in ['AOL', 'Ask']: search += '@gmail.com or @hotmail.com or @yahoo.com or @msn.com'
			elif web_search == 'Exalead': search += 'gmail.com'
			elif web_search == 'Lycos': search += '@hotmail.com or @yahoo.com or @gmail.com'
			elif web_search == 'Baidu': search += 'hotmail.com'
			else:	search += '*.com'
		operacion=re.match(r'(ip|filetype|site|mail):(.+) (.*)',search)
		if operacion:#si es un operador del tipo ':'
			if 'ip' in operacion.group(1):
				query+=ip(operacion.group(2).strip(),operacion.group(3).strip(),web_search)
			elif 'filetype' in operacion.group(1):
				query+=filetype(operacion.group(2).strip(),operacion.group(3).strip(),web_search)
			elif 'site' in operacion.group(1):
				query+=site(operacion.group(2).strip(),operacion.group(3).strip(),web_search)
			elif 'mail' in operacion.group(1):
				query+=mail(operacion.group(2).strip(),operacion.group(3).strip(),web_search)
		else:# si no es del tipo ':'
			operacion2=re.match(r'(.*)[-|+](.*)',search)
			if operacion2: #Si es operador include o exclude
				if '-' in search:
					query+=exclude(operacion2.group(2).strip(), buildQuery(operacion2.group(1).strip(),web_search), web_search)
				if '+' in search:
					query+=include(operacion2.group(2).strip(), buildQuery(operacion2.group(1).strip(),web_search), web_search)
				else:# Si entra pero no es ninguno sale error
					print('Existe un error de entrada')
			else:#Si no tiene ninguno de los operadores
				operacion3=re.match(r'\'(.*)\'',search)
				if operacion3:
					return '\''+operacion3.group(1)+'\''
				else:
					return re.sub(' ','+',search) #se manda una busqueda normal del tipo 'departamento+barato+cdmx'
	return query


def ip(ip,obj_search,web_search):
	"""Función que da formato a la búsqueda cuando se busca con el operador ip.
	Recibe: ip (dirección ip a buscar), obj_search (términos adicionales de búsqueda), web_search (motor de búsqueda)
	Devuelve: query (búsqueda del operador ip con formato para su motor de búsqueda correspondiente)"""
	#q=ip%3A192.168.190.10+local&oq=ip%3A192.168.190.10+local
	query=''
	if search=='':
		if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Baidu', 'Ask', 'Exalead', 'Ecosia']:   query+='ip%3A'+ip+'&oq=ip%'+ip
		elif web_search == 'Lycos': query+='ip+'+ip
	else:
		if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Baidu', 'Ask', 'Exalead', 'Ecosia']:   query+='ip%3A'+ip+'+'+obj_search
		elif web_search == 'Lycos': query+='ip+'+ip+'+'+obj_search
	return query

def filetype(tipo_archivo,obj_search,web_search):
	"""Función que da formato a la búsqueda cuando se busca con el operador filetype.
	Recibe: tipo_archivo (tipo de archivo a buscar), obj_search (términos adicionales de búsqueda), web_search (motor de búsqueda)
	Devuelve: query (búsqueda del operador filetype con formato para su motor de búsqueda correspondiente)"""
	#p=inurl%3A".pdf"+algo
	query=''
	if web_search in ['Google', 'Bing', 'Baidu', 'Ask', 'Exalead', 'Ecosia', 'Lycos', 'Yahoo']:	query += 'filetype%3A'+tipo_archivo+'+'+obj_search
	elif web_search == 'DuckDuckGo':	query += obj_search+'+filetype%3A.'+tipo_archivo+' inurl:'+tipo_archivo.split()[0]
	elif web_search == 'AOL': query+='filetype-'+tipo_archivo+'+'+obj_search

	return query

def site(site,obj_search,web_search):
	"""Función que da formato a la búsqueda cuando se busca con el operador site.
	Recibe: site (sitio donde se busca), obj_search (términos adicionales de búsqueda), web_search (motor de búsqueda)
	Devuelve: query (búsqueda del operador site con formato para su motor de búsqueda correspondiente)"""
	#q=site%3Astackoverflow.com+problem&oq=site%3Astackoverflow.com+problem
	#q=site%3Astackoverflow.com&oq=site%3Astackoverflow.com
	query=''
	if obj_search=='':
		if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Baidu', 'Ask', 'Exalead', 'Ecosia']:   query+='site%3A' + site+'&oq=site%3A'+site
		elif web_search == 'AOL': query+='site-'+site
		elif web_search == 'Lycos': query+='site+'+site
	else:
		if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Baidu', 'Ask', 'Exalead', 'Ecosia']:   query+='site%3A' + site+'+'+obj_search
		elif web_search == 'AOL': query+='site-'+site+'+'+obj_search
		elif web_search == 'Lycos': query+='site+'+site+'+'+obj_Search
	return query

def mail(mail,obj_search,web_search):
	"""Función que da formato a la búsqueda cuando se busca con el operador mail.
	Recibe: mail (dominio a buscar), obj_search (términos adicionales de búsqueda), web_search (motor de búsqueda)
	Devuelve: query (búsqueda del operador mail con formato para su motor de búsqueda correspondiente)"""
	#q=email%3Agmail.com+hi&oq=email%3Agmail.com+hi&
	query=''
	if obj_search=='':
		if web_search == 'Google':   query+='inurl%3A\"email.xls\"+intext%3A%40'+mail # inurl%3A"email.xls"+intext%3A%40gmail.com
		elif web_search == 'Baidu': query+='filteype%3Axls intext%3A%40'+mail
		elif web_search == 'DuckDuckGo': query+='inurl%3Axls+\"'+mail+'\"' # inurl%3Axls+"gmail.com"
		elif web_search in ['Ecosia', 'Ask', 'Bing', 'Lycos']: query+='filetype%3Axls+intext%3A%40'+mail # filetype%3Axls+intext%3A%40gmail.com
		elif web_search in ['Yahoo','AOL']:query+='filetype%3Axls+%40'+mail # filetype:xls @gmail.com
		elif web_search == 'Exalead': query+='inurl%3Axls+\"%40'+mail+'\"'
	else:
		if web_search == 'Google':   query+='inurl%3A\"email.xls\"+intext%3A%40'+mail+obj_search
		elif web_search == 'Baidu': query+='filteype%3Axls intext%3A%40'+mail+' '+obj_search
		elif web_search == 'DuckDuckGo': query+='inurl%3Axls+\"'+mail+'\"'+obj_search # inurl%3Axls+"gmail.com"
		elif web_search in ['Ecosia', 'Ask', 'Bing', 'Lycos']: query+='filetype%3Axls+intext%3A%40'+mail+obj_search # filetype%3Axls+intext%3A%40gmail.com
		elif web_search in ['Yahoo', 'AOL']:query+='filetype%3Axls+%40'+mail+'+'+obj_search # filetype:xls @gmail.com
		elif web_search == 'Exalead': query+='inurl%3Axls+\"$40'+mail+'\"'+obj_search
	return query

def exclude(palabra,obj_search,web_search):
	"""Función que da formato a la búsqueda cuando se busca con el operador -
	Recibe: palabra (palabra que se excluye al buscar), obj_search (términos adicionales de búsqueda), web_search (motor de búsqueda)
	Devuelve: query (búsqueda del operador - con formato para su motor de búsqueda correspondiente)"""
	#q=casa+-jardin&oq=casa+-jardin
	query=''
	if obj_search=='':
		if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Ask', 'AOL', 'Lycos', 'Ecosia', 'Exalead']:   query+='-'+ palabra
		elif web_search == 'Baidu':    query+='-('+ palabra + ')'
	else:
		if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Ask', 'AOL', 'Lycos', 'Ecosia', 'Exalead']:   query += obj_search+'+-'+ palabra
		elif web_search == 'Baidu':    query += obj_search+'+-('+ palabra + ')'
	return query

def include(palabra,obj_search,web_search):
	"""Función que da formato a la búsqueda cuando se busca con el operador +
	Recibe: palabra (palabra que se incluye al buscar), obj_search (términos adicionales de búsqueda), web_search (motor de búsqueda)
	Devuelve: query (búsqueda del operador + con formato para su motor de búsqueda correspondiente)"""
	#q=casa+-jardin&oq=casa+-jardin
	query=''
	if obj_search=='':
		if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Ask', 'AOL', 'Lycos', 'Ecosia', 'Exalead']:   query='%2B'+ palabra
		elif web_search == 'Baidu':    query='%2B('+ palabra + ')'
	else:
		if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Ask', 'AOL', 'Lycos', 'Ecosia', 'Exalead']:   query += obj_search+'+%2B'+ palabra
		elif web_search == 'Baidu':    query += obj_search+'+%2B('+ palabra + ')'
	return query

def op_and(objL_search,objR_search,web_search):
	"""Función que da formato a la búsqueda cuando se busca con el operador and
	Recibe: objL_search (palabra que va antes de AND), objR_search (palabra que va después de AND), web_search (motor de búsqueda)
	Devuelve: query (búsqueda del operador AND con formato para su motor de búsqueda correspondiente)"""
	#q=casa+AND+blanca+AND+jardin
	query=''
	if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Ask', 'Ecosia','Exalead', 'Lycos']:    query += objL_search+'+AND+'+ objR_search
	elif web_search == 'Baidu':    query += '('+objL_search+') ('+objR_search+')'
	elif web_search == 'AOL': query+=objL_search+'+and+'+objR_search
	return query

def op_or(objL_search,objR_search,web_search):
	"""Función que da formato a la búsqueda cuando se busca con el operador or
	Recibe: objL_search (palabra que va antes de OR), objR_search (palabra que va después de OR), web_search (motor de búsqueda)
	Devuelve: query (búsqueda del operador OR con formato para su motor de búsqueda correspondiente)"""
	#q=casa+AND+blanca+AND+jardin
	query=''
	if web_search in ['Google', 'DuckDuckGo', 'Bing', 'Yahoo', 'Ask','Ecosia']:    query += objL_search+'+OR+'+ objR_search
	elif web_search == 'Baidu':    query += '('+objL_search+'%7C'+objR_search+')'
	elif web_search == 'AOL': query+=objL_search+'+or+'+objR_search
	elif web_search == 'Exalead':    query += '('+objL_search+')+OR+('+objR_search+')'
	elif web_search == 'Lycos': query+= objL_search+'+%7C+'+objR_search
	return query
