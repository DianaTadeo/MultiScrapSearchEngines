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
class SearchGoogle:
    def __init__(self, query):
        self.query = 'search?q='+query

    def ip(self):
        pass

    def mail(self):
        pass

    def filetype(self,tipo_archivo):
        # as_filetype=extension
        self.query += '&as_filetype=' + tipo_archivo
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

search = 'prueba filetype:pdf site:www.google.com -uno +dos otroORnada nuevoANDviejo \'palabra\''
bus = [s for s in search.split(' ')]
busqueda = SearchGoogle(bus[0])
for op in bus:
    if 'site' in op:
        busqueda.site(op[6:])
    elif '-' in op:
        busqueda.exclude(op[1:])
    elif '+' in op:
        busqueda.include(op[1:])
    elif 'OR' in op:
        busqueda.op_or(op[:op.find('OR')],op[op.find('OR')+2:])
    elif 'AND' in op:
        busqueda.op_and(op[:op.find('AND')],op[op.find('AND')+3:])
    elif 'filetype' in op:
        busqueda.filetype(op[10:])

print bus
print busqueda.query
print 'https://google.com/'+busqueda.query
