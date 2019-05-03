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

-b BUSQUEDA -> obligatorio.

-n NUM_RESULTADOS -> opcional.

-p -> opcional  -> para inlcuir los parámetros GET de la URL.

-t -> opcional -> forzar cambio de dirección IP para realizar las peticiones.

-f FORMATO -> opcional -> indica el formato de salida txt, html o xml, por defecto los muestra en STDOUT.

-h -> muestra las opciones disponibles del script.

Una vez que se tiene los términos de la búsqueda a realizar, se hacen las peticiones a los 10 motores de búsqueda con Tor (localhost:9050).

Si en la respuesta que se obtiene se encuentra que la IP ha sido bloqueada, se realiza el cambio de la IP por otra mediante el ControlPort 9051 (se permite el control de la conexión con Tor Control Protocol)

En este módulo se hace uso de los otros dos módulos desarrollados, es decir, __busqueda.py__ para obtener la URL con el formato requerido por cada motor con la que se realizará el request y __reporte.py__ que analiza la respuesta obtenida de los motores de búsqueda para generar el reporte en el formato que se indique o para mostrarlo en la salida estándar.

### busqueda.py

### reporte.py

En este módulo se analiza la respuesta obtenida de los request a los motores de búsqueda para obtener los enlaces, dominios o correos de acuerdo al operador utilizado en la búsqueda.

Se hace uso de la biblioteca bs4 para una exracción más sencilla de los elementos requeridos y generar la salida correspondiente.

De acuerdo al motor de búsqueda, se hace la búsqueda de los enlaces para almacenar cada salida (de cada motor) en una lista que será utilizada para escribirlos en los archivo de salida correspondiente, o bien, en STDOUT.
