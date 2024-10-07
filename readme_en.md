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
I list the drivers necessary for those devices.

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

This screen allows you to configure the parameters with which execute 
the experiment. Each device has its own group box indicating what 
options can be modified.

![Configure Run](Documentation/configure_page.png "Configuration")

Camera: group box has a section showing continuously photos of the
device. You can also click on the screen to assign the translation unit movement.
This movement can be calibrated in the calibration screen.
The square/line selection indicates whether the engine
X and the engine and move in parallel or simultaneous respectively.

Calibration Screen: see instructions in the info button.

![Calibration Screen](Documentation/configure_page_calibration.png "Calibration")

Motor: Each motor has a current position and its parameters of
speed, acceleration and antiplay (backlash).
The motor can be zeroed
with the button.
During the run, the engine will go from the initial position to the final with
the amount of steps indicating the amount of stops.
Example: If the engine
x/y are in line mode with the parameters: initial 0, final 2, steps 3;
The positions will be (0.0), (1,1), (2,2).

Move Engine: This section allows you to send the engine to the position in
the input box on top. The bottom box saves the current position when the user
issues a move command.
Stop button stops the engine at once, in case that there is an error.

Function Generator: allows you to configure amplitude, offset,
the shape and frequency range.
All frequency values are in Hertz. The frequency range can be linear or logarithmic.
Example:
With parameters initial frequency 10, initial frequency 1000, steps 3
and logarithmic scale on; The frequencies will be 10, 100, 1000.

Oven: Allows you to configure the oven temperature range.

Focus Control: Allows you to turn on and off the laser probe , 
control it's power and see the reflectance graphics,
 ABCD sum and focus error.
Focus control automatically focuses
the engine moving the Z axis with the parameters provided (non-functional).

![Focus Control Graphs](Documentation/configure_page_dac_graphs.png)

Lockin: Allows you to configure the time constant, the input gain, the slope,
the harmonic and external reference.
Important: For experiments, the external reference should always be on.

![Lock-in Graphs](Documentation/configure_page_lockin_graphs.png)

Coupling: It allows to indicate which devices are coupled and the order
of the points.
The devices with the highest value cycle their points first.
Example: If the ovens coupling is 1 with the values
40 ° and 50 ° and the function generators coupling is 2 with the values
100Hz and 1000Hz The points are (40 °, 100Hz) -> (40 °, 1000Hz)
-> (50 °, 100Hz) -> (50 °, 1000Hz).

### Executing Run

This screen allows you to monitor the progress of the experiment run.
The graphs show the phase (°/log (Hz)) and amplitude (log (v)/log (Hz)).
The "stop" button aborts the execution of the program.

![Executing Run](Documentation/running_page.png "Run")

### Data table

This screen allows you to see the final data of the experiment. Up to the
left you can save the information of the variables, indicating
what the meaning and unit of each one.
Up to the right you can save the data table, both in matlab format and csv format.

![Final Data Table](Documentation/data_page.png "Data")
