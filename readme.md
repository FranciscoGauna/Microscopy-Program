# Microscopy-Program
## Resumen
Este programa es un software cuyo objetivo es controlar el 
microscopio fototérmico desarrollado por Facundo Zaldivar Escola.

## Instalación
### Python

La version de python utilizada para el desarrollo fue Python 3.11.4.
Se puede descargar del siguiente link https://www.anaconda.com/download.

### Biblioteca

Para instalar las bibliotecas de python es solo necesario hacer el comando `pip install -r requirements.txt`. 
Proveo también el archivo `frozenreqs.txt` que contienen la version específica de las bibliotecas de python
con las cuales se testeó y utilizo el programa.

### Dispositivos Externos

El funcionamiento del Microscopy-Program depende de drivers de dispositivos externos. Listo los drivers utilizados.

Lock-in AMU 2.4: [`AMU 2.4 Lockin.dll` de Anfatec](https://www.anfatec.de/products/3_lockin/amu/24/pci-bus_lockin_amplifier_amu24.html)

Platina:[`XIMC Software Package` de Standa](https://files.xisupport.com/Software.en.html)

Camara: [`LgCam Software` de Lumenera](https://www.lumenera.com/support/industrial-usb-ethernet/drivers-downloads.html)

DAQ: [`MCCDAQ` de Diligent](https://cloud.digilent.com/myproducts/ULxforWindows?pc=1&tab=2)

## Utilizacion
### Seleccionar Dispositivos

Esta pantalla permite seleccionar que instancia de dispositivos se quieren 
utilizar. "Virtual" indica que este dispositivo no va a conectarse a un
dispositivo real, sino que va a utilizar un driver que pretende estar conectado.

Los siguientes dispositivos están disponibles para los siguientes tipos de 
dispositivos:

Generador de Funciones:
- HP 33120A
- Rigol DG1022

Amplificador Lock-in:
- Anfatec AMU 2.4
- NF LI5660

Platina:  
La platina soporta cualquier motor conectado que responda al xilab.

Camara:
- Lumenera Infinity 1
- Web Cam controlada por CV2

Horno:
- Linkam TM 94

Digital-to-Analog-Converter (DAC):
- MCC USB-2527

Una vez seleccionado los dispositivos lanzar inizaliza los dispositivos

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