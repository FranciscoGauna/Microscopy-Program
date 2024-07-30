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

## Utilización
### Seleccionar Dispositivos

Esta pantalla permite seleccionar que instancia de dispositivos se quieren 
utilizar. 

![Seleccion de Dispositivos](Documentation/choose_devices.png 
"Dispositivos")

"Virtual" indica que este dispositivo no va a conectarse a un
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

Los motores de la platina pueden ser cargados con archivos de configuracion
provistos por xilab para ese motor especifico. Estos incluyen informacion
sobre el feedback, si la direccion positiva esta invertida y sobre la
relacion entre cuentas del motor y la distancia real. Si se tiene esta ultima
la pantalla siguiente muestra la posicion en la unidad indicada.

Una vez seleccionado los dispositivos lanzar inizaliza los dispositivos.

#### Configuración de Conexión

Cada dispositivo provisto tiene diferentes métodos de conexión.
En el caso de la camara web, el generador de funciones HP 33120A, 
el horno Linkam y la placa DAC USB tienen parámetros de conexión dependientes
de como esten conectados. Estos se pueden configurar en el archivo `devices.ini`
que es generado con valores por defecto cuando se corre el programa 
por primera vez.


### Configurar Corrida

Esta pantalla permite configurar los parámetros con los cuales se va a 
ejecutar el experimento. Cada dispositivo tiene su propio grupo de controles
indicando que opciones se pueden modificar.

![Configurar Corrida](Documentation/configure_page.png 
"Configuración")

Camara: La camara tiene un cuadrado mostrando continuamente fotos del
dispositivo. Se puede ademas clickear en la pantalla para asignar 
la ruta de movimiento de la platina. Este movimiento se puede calibrar
con el boton calibrar. La seleccion de cuadrado/linea indica si el motor
x y el motor y se mueven en paralelo o simultaneo respectivamente.

Pantalla de calibracion:

Motor: Cada motor tiene una posicion actual y sus parametros de
velocidad, aceleracion y antiplay (backlash). Se puede cambiar el cero
con el boton que indica que la posicion actual es el cero. Durante
la corrida, el motor va a ir de la posicion inicial a la final con
la cantidad de pasos indicando cuantas paradas hace. Ejemplo: si el motor
x/y estan en modo linea con los parametros: inicial 0, final 2, pasos 3; 
las posiciones van a ser (0,0), (1,1), (2,2).

Mover Motor: esta seccion permite enviar el motor a la posicion en
la caja de arriba. La caja de abajo guarda la posicion en la cual 
estaba cuando se movio. Stop para el motor en el momento, en caso de
que haya un error. 

Generador de Funciones: permite configurar la amplitud, el offset, 
la forma y el rango de frecuencias. Todos los valores de frecuencias
son en Hertz.
El rango de frecuencias puede ser lineal o logaritmico. Ejemplo:
Con los parametros frecuencia inicial 10, frecuencia inicial 1000,
pasos 3; las freucncias van a ser 10, 100, 1000.

[//]: # (Actualizar texto en screenshot y remover repeat)

Horno: permite configurar el rango de temperatura del horno.

Control de Foco: permite prender y apagar el control laser
de prueba, controlar su potencia y ver los graficos de reflectancia, 
suma abcd y error de foco. El control de foco automaticamente enfoca
el motor moviendo el eje Z con los parametros provistos (no funcional).

[//]: # (Sacar foto de los graficos)

Lockin: permite configurar la constante de tiempo, la ganancia, la curva,
el harmonico y la referencia externa. Importante: para los experimentos, la
referencia externa tendria que estar siempre prendida.

[//]: # (Sacar foto de grafico y)

Acoplamiento: permite indicar que dispositivos están acoplados y el orden 
de los puntos. Los dispositivos con el valor más alto varian sus puntos 
primero. Ejemplo: si la el horno está acoplado en 1 con los valores
40° y 50° y el generador de frecuencia esta acoplado en 2 con los valores
100Hz y 1000Hz los puntos son (40°, 100Hz) -> (40°, 1000Hz)
 -> (50°, 100Hz) -> (50°, 1000Hz).



### Ver Corrida
![Ver Corrida](Documentation/running_page.png 
"Corrida")

### Tabla de Datos
![Tabla de Datos Final](Documentation/data_page.png 
"Datos")