# ProyectoModulo3
## Integrantes:
* Tadeo Guillén Diana Guadalupe
* Vallejo Fernández Rafael Alejandro

### Detalles del proyecto:

El proyecto consiste en un scraper que pueda ser ejecutado en plataformas GNU/Linux.

El lenguaje con el que fue desarrollado el proyecto fue Python 2.7 y desarrollamos 3 módulos para cubrir cada uno de los requisitos solicitados.

Las módulos externos de Python que se requieren para el correcto funcionamiento del script se encuentran en el archivo __requirements.txt__ y para instalarlo:
```bash
sudo pip install -r requirements.txt
```

Otro requisito es tener instalado Tor y para ello las instrucciones de instalación y configuración se encuentran en __torInstall.sh__

Los módulos desarrollados fueron: __anonimizacion.py, busqueda.py y reporte.py__.

Una vez que se han instalado y configurado las dependencias adicionales, el script (módulo principal) que debe ser ejecutado para obtener los resultados es: __anonimizacion.py__

### anonimizacion.py
En este módulo se leen los argumentos de ejecución del script que indican:

__-b BUSQUEDA__ -> obligatorio.

__-n NUM_RESULTADOS__ -> opcional.

__-p__ -> opcional  -> para inlcuir los parámetros GET de la URL.

__-t__ -> opcional -> forzar cambio de dirección IP para realizar las peticiones.

__-f FORMATO__ -> opcional -> indica el formato de salida txt, html o xml, por defecto los muestra en STDOUT.

__-h__ -> muestra las opciones disponibles del script.

Una vez que se tienen los términos de la búsqueda a realizar, se hacen las peticiones a los 10 motores de búsqueda con Tor (localhost:9050).

Si en la respuesta que se obtiene se encuentra que la IP ha sido bloqueada, se realiza el cambio de la IP por otra mediante el ControlPort 9051 (se permite el control de la conexión con Tor Control Protocol)

En este módulo se hace uso de los otros dos módulos desarrollados, es decir, __busqueda.py__ para obtener la URL con el formato requerido por cada motor con la que se realizará el request y __reporte.py__ que analiza la respuesta obtenida de los motores de búsqueda para generar el reporte en el formato que se indique o para mostrarlo en la salida estándar.

### busqueda.py
En el módulo __busqueda.py__ se genera la URL con la que se hará el request y para ello, en este módulo, se recibe la búsqueda ingresada por argumentos y se le aplican los operadores que se solicitaron, es decir, si está alguno de los siguientes:

__ip:<dirección_ip>__

__mail[:<dominio>]__

__filetype:<tipo_archivo>__

__site:<dominio>__

__-<palabra>__

__+<palabra>__

__<op1> AND <op2>__

__<op1> OR <op2>__

__‘<palabra>’__

Se recorre la búsqueda recursivamente para obtener el formato completo y posteriormente formar la URL correspondiente.

De acuerdo al motor que se esté utilizando en ese momento, se le pasa el número de resultados a buscar para obtener una mayor cantidad de resultados.

### reporte.py

En este módulo se analiza la respuesta obtenida de los request a los motores de búsqueda para obtener los enlaces, dominios o correos de acuerdo al operador utilizado en la búsqueda.

Se hace uso de la biblioteca bs4 para una extracción más sencilla de los elementos requeridos y generar la salida correspondiente.

De acuerdo al motor de búsqueda, se hace la búsqueda de los enlaces para almacenar cada salida (de cada motor) en una lista que será utilizada para escribirlos en el archivo de salida correspondiente, o bien, en STDOUT.

Para cada formato de salida (txt, html, xml) se toma la lista obtenida de cada búsqueda y cada motor y se escribe en el archivo __Busquedas.txt__, __Busquedas.html__ o __Busquedas.xml__, respectivamente.

Si el archivo ya existe, se agregan los resultados obtenidos de las nuevas búsquedas realizadas.
