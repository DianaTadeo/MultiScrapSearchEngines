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


USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')
	#q=filetype%3Axml+correos&oq=filetype%3Axml+correos
    google_url = 'https://www.google.com/{}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text.encode('utf-8')

class SearchGoogle:
    def __init__(self, search):
        self.search = search
        self.query= 'search?q='
	#ip%3A192.168.190.10+local&oq=ip%3A192.168.190.10+local
    def ip(self,ip):
		if search=="":
			self.query+='ip%3A'+ip+'&oq=ip%'+ip
		else:
			self.query+='ip%3A'+ip+'+'+self.search+'&oq=ip%'+ip+'+'+self.search
		return self.query

    def mail(self):
        pass

    def filetype(self,tipo_archivo):
        # as_filetype=extension
        self.query += 'filetype%3A' + tipo_archivo+'+'+self.search+'&oq=filetype%3Axml'+'+'+self.search
        return self.query

    def site(self, sitio):
        # as_sitesearch=example.com
        self.query += '&as_sitesearch=' + sitio
        return self.query

    def exclude(self, palabra):
        # q=query+goes+here&as_eq=don't+include+these+words
        self.query += '&as_eq=' + palabra
        return self.query

    def include(self, palabra):
        # q=query+goes+here%2Bterm
        self.query += '%2B' + palabra
        return self.query

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

#solo funciona para ip y para filetype por separado
search = 'prueba ip:192.168.129.24'
bus = [s for s in search.split(' ')]
busqueda = SearchGoogle(bus[0])
for op in bus:
	#print op
	if 'ip' in op:
		busqueda.ip(op[3:])
	if 'site' in op:
		busqueda.site(op[6:])
	if '-' in op:
		busqueda.exclude(op[1:])
	if '+' in op:
		busqueda.include(op[1:])
	if 'OR' in op:
		busqueda.op_or(op[:op.find('OR')],op[op.find('OR')+2:])
	if 'AND' in op:
		busqueda.op_and(op[:op.find('AND')],op[op.find('AND')+3:])
	if 'filetype' in op:
		busqueda.filetype(op[9:])
        
if __name__ == '__main__':
    keyword, html = fetch_results(busqueda.query, 20, 'en')
    print(html)
    #print bus
    #print busqueda.query
    #print 'https://google.com/'+busqueda.query
