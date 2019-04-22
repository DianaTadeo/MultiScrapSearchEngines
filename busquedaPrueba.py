#!/usr/bin/python
# -*- coding: utf-8 -*-
# Motores de búsqueda:
# 1. Google : https://google.com/search?q=
# 2. Bing :
# 3. Yahoo
# 4. Ask.com
# 5. AOL.com
# 6. Baidu
# 7. DuckDuckGo
import requests
import re
from bs4 import BeautifulSoup

#user agent de ejemplo
USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
    #url a la que se hara el request... en el primer {} va a ir el query
    google_url = 'https://www.google.com/{}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text.encode('utf-8')#a[un no resuelvo bien esto de la codificacion, pero con este hay salida
    
def buildQuery(search, browser):
	query='search?q='
	bus = [s for s in search.split(' ')]
	for op in bus:
		if 'ip' in op:
			query+=ip(op[3:],bus[0],browser)
		if 'filetype' in op:
			query+=filetype(op[9:],bus[0],browser)
		if 'site' in op:
			query+=site(op[5:],bus[0],browser)
		if 'mail' in op:
			query+=mail(op[5:],bus[0],browser)
		if '-' in op:
			query+=exclude(op[1:], bus[0], browser)
		if '+' in op:
			query+=include(op[1:], bus[0], browser)
	return query


def ip(ip,obj_search,browser):
	#q=ip%3A192.168.190.10+local&oq=ip%3A192.168.190.10+local
	query=''
	if search=='':
		query+='ip%3A'+ip+'&oq=ip%'+ip
	else:
		query+='ip%3A'+ip+'+'+obj_search+'&oq=ip%'+ip+'+'+obj_search
	return query

def filetype(tipo_archivo,obj_search,browser):
	#q=filetype%3Axml+correos&oq=filetype%3Axml+correos
	query=''
	query += 'filetype%3A' + tipo_archivo+'+'+obj_search+'&oq=filetype%3Axml'+'+'+obj_search
	return query

def site(site,obj_search,browser):
	#q=site%3Astackoverflow.com+problem&oq=site%3Astackoverflow.com+problem
	#q=site%3Astackoverflow.com&oq=site%3Astackoverflow.com
	query=''
	if search=='':
		query+='site%3A' + site+'&oq=site%3A'+site
	else:
		query+='site%3A' + site+'+'+obj_search+'&oq=site%3A'+site+'+'+obj_search
	return query
	
def mail(mail,obj_search,browser):
	#q=email%3Agmail.com+hi&oq=email%3Agmail.com+hi&
	query=''
	if search=='':
		query+='email%3A'+mail+'&oq=email%3A'+mail
	else:
		query+='email%3A'+mail+'+'+obj_search+'&oq=email%3A'+mail+'+'+obj_search
	return query
  
def exclude(palabra,obj_search,browser):
	#q=casa+-jardin&oq=casa+-jardin
	query=''
	query += obj_search+'+-'+ palabra+'&oq='+obj_search+'+-'+palabra
	return query
def include(palabra,obj_search,browser):
	#q=casa+-jardin&oq=casa+-jardin
	query=''
	query += obj_search+'+%2B'+ palabra+'&oq='+obj_search+'+%2B'+palabra
	return query
  
""" 
    def op_and(self, op1, op2):
        # query+AND+string
        self.query += '&%s+AND+%s' % (op1, op2)
        return self.query

    def op_or(self, op1, op2):
        # as_oq="query+string"+goes+here
        self.query += '&as_oq=%s+%s' % (op1, op2)
        return self.query

    def quotation(self, palabra):
        # as_epq=query+goes+here
        self.query += '&as_epq=' + palabra
        return self.query
"""
#-------------------Para probar----------------
# redirige la salida a un archivo.html y sevisa la salida de la busqueda

#search = 'algo ip:192.168.201.45'
#seacrh = 'problem filetype:pdf'
#search = 'alumnos site:fciencias.unam.mx'
#search = 'something mail:gmail.com'
#search = 'Benito -Juarez'
search = 'Benito +Juarez'

"""
	if 'OR' in op:
		busqueda.op_or(op[:op.find('OR')],op[op.find('OR')+2:])
	if 'AND' in op:
		busqueda.op_and(op[:op.find('AND')],op[op.find('AND')+3:])
"""
        
if __name__ == '__main__':
	
    keyword, html = fetch_results(buildQuery(search, ''), 20, 'en')# 20 es el numero de resultados, se puede cambiar, en es el idioma
    #print buildQuery(search, '')
    print(html)
    #print bus
    
    #print 'https://google.com/'+busqueda.query
