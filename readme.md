# Microscopy-Program
## Resumen
Este programa es un software cuyo objetivo es controlar el 
microscopio fototérmico desarrollado por Facundo Zaldivar Escola.

## Instalación
### Python

La version de python utilizada para el desarrollo fue Python 3.11.4.
Se puede descargar del siguiente link https://www.anaconda.com/download.

### Librerias

Para instalar las librerias de python es solo necesario hacer el comando `pip install -r requirements.txt`. 
Proveo también el archivo `frozenreqs.txt` que contienen la version especifica de las librerias de python
con las cuales se testeó y utilizo el programa.

### Dispositivos Externos

El funcionamiento del Microscopy-Program depende de drivers de dispositivos externos. Listo los drivers utilizados.

Platina:[`XIMC Software Package` de Standa](https://files.xisupport.com/Software.en.html)

Camara: [`LgCam Software` de Lumenera](https://www.lumenera.com/support/industrial-usb-ethernet/drivers-downloads.html)

DAQ: [`MCCDAQ` de Diligent](https://cloud.digilent.com/myproducts/ULxforWindows?pc=1&tab=2)

## Utilizacion
### Seleccionar Dispositivos
![Seleccion de Dispositivos](Documentation/choose_devices.png 
"Dispositivos")

### Configurar Corrida
![Configurar Corrida](Documentation/configure_page.png 
"Configuración")

### Ver Corrida
![Ver Corrida](Documentation/running_page.png 
"Corrida")

### Tabla de Datos
![Tabla de Datos Final](Documentation/data_page.png 
"Datos")