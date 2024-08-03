<!-- TRANSLATED by md-translate -->
# Microscopy-Program

## Summary

This program is software whose objective is to control the
Photothermal microscope developed by Facundo Zaldivar Escola.

## Installing

### Python

The Python version used for development was Python 3.11.4.
You can download from the following link https://www.anaconda.com/download.

### Libraries

To install Python libraries, it is only necessary to make the command
`pip install -r requirements.txt`.
I also provide the `frozenreqs.txt` file which contains the specific 
version of Python libraries with which the program was tested and used.

### External Devices

The operation of the Microscopy-Program depends on drivers of external devices.
I list the drivers necesary for those devices.

Lock-in AMU 2.4: [`AMU 2.4 Lockin.dll` from Anfatec](https://www.anfatec.de/products/3_lockin/amu/24/pci-bus_lockin_amplifier_amu24.html)

Translation Stage:[`XIMC Software Package` from Standa](https://files.xisupport.com/Software.en.html)

Camera: [`LgCam Software` from Lumenera](https://www.lumenera.com/support/industrial-usb-ethernet/drivers-downloads.html)

DAQ: [`MCCDAQ` from Diligent](https://cloud.digilent.com/myproducts/ULxforWindows?pc=1&amp;tab=2)


## Use

Note: See also Documentation of [SER](https://github.com/FranciscoGauna/SER)
For more details about the use of this software. This documentation
focuses on the relevant details to the devices associated with
experimental setup associated with the photothermic microscope of the
Laboratorio de Haces Dirigidos in the Facultad de Ingenieria in the 
Universidad de Buenos Aires.

### Select devices


This screen allows you to select which kind of device to use.

![Device selection](documentation/choose_devices.png "Devices")

"Virtual" indicates that this device will not connect to a
real device, but will use a mock driver.


The following devices are available for the following types of
devices:

Function Generator:

* HP 33120A
* Rigol DG1022

Lock-in Amplifier:

* Anfatec AMU 2.4
* NF LI5660

Translation Unit: supports any connected engine that responds to the Xilab.

Camera:

* Lumenera Infinity 1
* Webcam controlled by CV2

Oven:

* Linkam TM 94

Digital-To-Analog-Converter (DAC):

* MCC USB-2527

Translation unit motors can be configured with files
provided by Xilab for that specific motor.
These include information on feedback, if the direction is reversed and 
the conversion factor between motor counts and real distance.
If you have the latter the following screen will display
the position in the provided units.

Once the devices have been selected, Launch initiates devices.

#### Connection Configuration

Each device provided has different connection methods.
In the case of the webcam, the function generator HP 33120A,
the linkam oven and the USB DAC plate they have parameters
dictating how they are connected.
These can be configured in the `devices.ini` file
which is generated with default values when the program runs
for the first time.

### Configure Run

Esta pantalla permite configurar los parámetros con los cuales se va a 
ejecutar el experimento. Cada dispositivo tiene su propio grupo de controles
indicando que opciones se pueden modificar.

This screen allows you to configure the parameters with which
Execute the experiment.
Each device has its own control group
indicating what options can be modified.

![Configure Run](Documentation/configure_page.png "Configuration")

Camera: group box has a section showing continuously photos of the
device. You can also click on the screen to assign the translation unit movement.
This movement can be calibrated in the calibration screen.
The square/line selection indicates whether the engine
X and the engine and move in parallel or simultaneous respectively.

Pantalla de calibración:

Calibration screen:

![Pantalla de Calibración](Documentation/configure_page_calibration.png)

! [Calibration screen] (Documentation/configure_page_calibration.png)

Motor: Cada motor tiene una posición actual y sus parámetros de
velocidad, aceleración y antiplay (backlash). Se puede cambiar el cero
con el botón que indica que la posición actual es el cero. Durante
la corrida, el motor va a ir de la posición inicial a la final con
la cantidad de pasos indicando cuantas paradas hace. Ejemplo: si el motor
x/y están en modo línea con los parámetros: inicial 0, final 2, pasos 3; 
las posiciones van a ser (0,0), (1,1), (2,2).

Motor: Each engine has a current position and its parameters of
speed, acceleration and antiplay (backlash).
Zero can be changed
With the button that indicates that the current position is zero.
During
The run, the engine will go from the initial position to the final with
The amount of steps indicating how many stops ago.
Example: If the engine
x/y are in line mode with the parameters: initial 0, final 2, steps 3;
The positions will be (0.0), (1,1), (2,2).

Mover Motor: esta sección permite enviar el motor a la posición en
la caja de arriba. La caja de abajo guarda la posición en la cual 
estaba cuando se movió. Stop para el motor en el momento, en caso de
que haya un error.

MOVE ENGINE: This section allows you to send the engine to the position in
The box above.
The box below keeps the position in which
It was when he moved.
Stop for the engine at the time, in case of
That there is an error.

Generador de Funciones: permite configurar la amplitud, el offset, 
la forma y el rango de frecuencias. Todos los valores de frecuencias
son en Hertz.
El rango de frecuencias puede ser lineal o logarítmico. Ejemplo:
Con los parámetros frecuencia inicial 10, frecuencia inicial 1000,
pasos 3; las frecuencias van a ser 10, 100, 1000.

Function generator: allows you to configure amplitude, offset,
The form and frequency range.
All frequency values
They are in Hertz.
The frequency range can be linear or logarithmic.
Example:
With parameters initial frequency 10, initial frequency 1000,
Steps 3;
The frequencies will be 10, 100, 1000.

Horno: permite configurar el rango de temperatura del horno.

Oven: Allows you to configure the oven temperature range.

Control de Foco: permite prender y apagar el control laser
de prueba, controlar su potencia y ver los gráficos de reflectancia, 
suma abcd y error de foco. El control de foco automáticamente enfoca
el motor moviendo el eje Z con los parámetros provistos (no funcional).

FOCUS CONTROL: Allows you to turn on and off laser control
of proof, control your power and see the reflectance graphics,
Sum ABCD and focus error.
Focus control automatically focuses
The engine moving the Z axis with the parameters provided (non -functional).

![Graficos Control de Foco](Documentation/configure_page_dac_graphs.png)

! [FOCUS CONTROL GRAPHICS] (DOCUMENTATION/CONFIGURE_PAGE_DAC_GRAPHS.PNG)

Lockin: permite configurar la constante de tiempo, la ganancia, la curva,
el armónico y la referencia externa. Importante: para los experimentos, la
referencia externa tendría que estar siempre prendida.

Lockin: Allows you to configure the time constant, the gain, the curve,
The harmonic and external reference.
Important: For experiments, the
External reference should always be lit.

![Graficos Lock-in](Documentation/configure_page_lockin_graphs.png)

! [LOCK-IN] (Documentation/Configure_Page_Lockin_graphs.png)

Acoplamiento: permite indicar qué dispositivos están acoplados y el orden 
de los puntos. Los dispositivos con el valor más alto varían sus puntos 
primero. Ejemplo: si la el horno está acoplado en 1 con los valores
40° y 50° y el generador de frecuencia está acoplado en 2 con los valores
100Hz y 1000Hz los puntos son (40°, 100Hz) -> (40°, 1000Hz)
 -> (50°, 100Hz) -> (50°, 1000Hz).

Coupling: It allows to indicate which devices are coupled and the order
of the points.
The devices with the highest value vary their points
first.
Example: If the oven is coupled in 1 with the values
40 ° and 50 ° and the frequency generator is coupled in 2 with the values
100Hz and 1000Hz The points are (40 °, 100Hz) -> (40 °, 1000Hz)
-> (50 °, 100Hz) -> (50 °, 1000Hz).

### Ver Corrida

### See run

Esta pantalla permite monitorear el progreso de la corrida del experimento.
Los graficos muestran los valores de fase (°/log(Hz)) y 
amplitud (log(V)/log(Hz)). El boton de "Parar" aborta la ejecuccion del
programa.

This screen allows you to monitor the progress of the experiment run.
The graphs show the phase (°/log (Hz)) and
amplitude (log (v)/log (Hz)).
The "stop" button abort the execution of the
program.

![Ver Corrida](Documentation/running_page.png "Corrida")

! [See run] (documentation/running_page.png "run")

### Tabla de Datos

### Data table

Esta pantalla permite ver los datos finales del experimento. Arriba a la 
izquierda se puede guardar la información de las variables, indicando
que significa cada valor y su unidad. Arriba a la derecha se puede
guardar la tabla de datos, tanto en formato matlab como formato
csv (comma separated values).

This screen allows you to see the final data of the experiment.
Up to the
left you can save the information of the variables, indicating
What does each value and its unit mean.
Up to the right you can
save the data table, both in matlab format and format
CSV.

![Tabla de Datos Final](Documentation/data_page.png "Datos")

! [Final Data Table] (Documentation/Data_Page.png "Data")