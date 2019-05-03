#!/usr/bin/python
# -*- coding: utf-8 -*-

from requests import Session  # session para realizar las peticiones mediante TOR  # pip install requests
from requests.exceptions import ConnectionError
import requests
from stem import Signal  # pip install stem
from stem.control import Controller
from random import choice
from time import sleep
from sys import exit,stderr
import argparse
import reporte
import busqueda
# /etc/tor/torrc -> ControlPort 9051 ->
# NOTA: control requiere privilegios

def printError(msg, eexit = False):
	"""Función que imprime mensaje de error y sale del programa
	Recibe: mensaje a mostrar y booleano que indica si se debe terminar la ejecución del programa"""
	stderr.write('Error:\t%s\n' % msg)
	if eexit:
		exit(1)

def addOptions():
	"""
	Función para agregar las opciones al script
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument('-p','--params', action='store_true', dest='param', default=False, help='Resultados con parámetros GET.')
	parser.add_argument('-b','--busqueda', dest='busqueda', default=None, help='Busqueda que se va a realizar entre comillas dobles.')
	parser.add_argument('-n', '--number_results', dest= 'number_results', type=int, default=50, help ='Indica el número de resultados a buscar (10, 20, 30, 40, ..., 100).')
	parser.add_argument('-t', '--tor', action='store_true', dest = 'tor', default = False, help = 'Se cambia la dirección IP.')
	parser.add_argument('-f', '--formato', dest= 'formato', help ='El formato que toma para regresar el reporte "html", "xml" o "txt".')

	opts = parser.parse_args()
	return opts

def checkOptions(options):
	"""Función que verifica el estado de ciertas opciones para poder ejecutar el script"""
	if options.busqueda is None:
		printError('No se indicó la búsqueda a realizar.', True)

def getInfoRequest(session, header):
	"""
	Función que obtiene la IP desde la que se hace la petición y el agente de usuario.
	Recibe: objeto session (Session para hacer los request) y los header (para agente de usuario)
	Devuelve: en salida estándar muestra la IP actual y el agente de usuario
	"""
	ip = session.get('http://httpbin.org/ip', headers = header)  # Se obtiene la ip desde la que se hace la petición
	ip = str(ip.text).replace('  "origin\":','').replace('{','').replace('}','').replace('\n','').replace(',','\"')
	ip = ip[:ip.find('\"',2)+1]

	agente = session.get('http://httpbin.org/user-agent', headers = header)  # Se obtiene el agente de usuario con el que se hace la petición

	agente= str(agente.text).replace('  \"user-agent\":','').replace('{','').replace('}','').replace('\n','')

	print 'La petición se realiza desde:%s' % (ip)
	print 'El agente de usuario es:%s' % (agente)


def changeIP():
	"""Función para cambiar la dirección IP desde la que se hace la petición (se hacen desde Tor).
	Recibe: vacío. Devuelve: vacío (controller asigna la nueva dirección IP)
	"""
	with Controller.from_port(port = 9051) as controller:
		controller.authenticate()
		controller.signal(Signal.NEWNYM)

def makeRequest(search, search_engine, printInfoIP, number_results = 50):
	"""Función que realiza las peticiones anónimas.
	Recibe: search (busqueda a realizar en loa motores)
			search_engine (motor en donde realiza la búsqueda)
			printInfoIP (bool que indica si se muestra la dirección IP y el Agent-User)
			number_results (número de resultados que se arrojará por motor)
	"""
	# User Agent list: https://udger.com/resources/ua-list
	user_agent = [
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',  # Chrome
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0',  # Firefox
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 OPR/32.0.1948.25',  # Opera
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15',  # Safari
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 UBrowser/5.4.5426.1034 Safari/537.36',  # UC Browser
		'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Mercury/3.4 Mobile/10A523 Safari/8536.25',  # Mercury
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3739.0 Safari/537.36 Edge/75.0.109.0'  # Microsoft Edge
	]
	url = busqueda.fetch_results(busqueda.buildQuery(search, search_engine), search_engine, number_results)
	print url
	while True:
		session = Session()
		header = {'User-agent':choice(user_agent)}  # Valor que se agrega al diccionario para cambiar el agente
		session.proxies = {}
		if search_engine is 'Google':
			session.proxies['http'] = ''  # Proxy para petición a Google, no se hace petición anónima
			session.proxies['https'] = ''
		else:
			session.proxies['http'] = 'socks5://localhost:9050'  # Proxy http y https para realizar la petición mediante TOR
			session.proxies['https'] = 'socks5://localhost:9050'
		#---------Session prepare_request--------------
		response = requests.Request('GET', url, headers=header)
		prepared = session.prepare_request(response)
		resp = session.send(prepared, timeout = 15)

		if printInfoIP:	getInfoRequest(session, header)
		if 'class="g-recaptcha"' in resp.text.encode('utf-8'):
			print "HAY CAPTCHA en %s" % search_engine
		if 'class="g-recaptcha"' not in resp.text.encode('utf-8') and resp.status_code == 200:
			return url, resp.text.encode('utf-8')
		else:
			changeIP()
			getInfoRequest(session, header)
			print "Se cambió IP"
			sleep(5)

if __name__ == '__main__':
	try:
		opts = addOptions()
		checkOptions(opts)
		print 'La búsqueda es: %s' % opts.busqueda
		search_engines = ['Ecosia', 'Bing', 'Baidu', 'Yahoo', 'DuckDuckGo', 'AOL', 'Ask', 'Exalead', 'Lycos', 'Google']
		#search_engines = ['Lycos', 'Yahoo']
		search = opts.busqueda
		printInfoIP = True
		if opts.tor:  # Para pruebas de cambio de IP con tor
			changeIP()
		for search_engine in search_engines:
			try:
				if search_engine in ['Ask', 'AOL', 'Ecosia', 'Exalead']:
					pages = opts.number_results/10 # Number results ->50 / 10 = 5
					for page in range(pages):
						if search_engine == 'Ask': res = page+1
						elif search_engine in ['AOL', 'Ecosia', 'Exalead']: res = page
						url, query = makeRequest(search, search_engine, printInfoIP, res)
						print '%s: %s' % (search_engine, url)  # Para debug
						reporte.busquedaReporte(search, query, search_engine, opts.param, opts.formato)
						printInfoIP = False
				else:
					url, query = makeRequest(search, search_engine, printInfoIP, opts.number_results)
					print '%s: %s' % (search_engine, url)  # Para debug
					reporte.busquedaReporte(search, query, search_engine, opts.param, opts.formato)
			except Exception as e:
				print e #'Ocurrió un error para este motor.'
				continue
			printInfoIP = False

	except Exception as e:
		printError('Ocurrio un error inesperado')
		printError(e, True)
