# Manual del Desarrollador - Microscopy-Program

## Tabla de Contenidos

1. [Introduccion](#1-introduccion)
2. [Descripcion General de la Arquitectura](#2-descripcion-general-de-la-arquitectura)
3. [Estructura del Proyecto](#3-estructura-del-proyecto)
4. [Stack Tecnologico](#4-stack-tecnologico)
5. [Frameworks Principales](#5-frameworks-principales)
6. [Sistema de Componentes](#6-sistema-de-componentes)
7. [Referencia de Componentes de Hardware](#7-referencia-de-componentes-de-hardware)
8. [Flujo de Datos y Ciclo de Vida de la Aplicacion](#8-flujo-de-datos-y-ciclo-de-vida-de-la-aplicacion)
9. [Modelo de Hilos](#9-modelo-de-hilos)
10. [Agregar Nuevos Componentes](#10-agregar-nuevos-componentes)
11. [Sistema de Configuracion](#11-sistema-de-configuracion)
12. [Pruebas y Desarrollo](#12-pruebas-y-desarrollo)
13. [Patrones Comunes y Buenas Practicas](#13-patrones-comunes-y-buenas-practicas)
14. [Solucion de Problemas de Desarrollo](#14-solucion-de-problemas-de-desarrollo)
15. [Recursos Externos](#15-recursos-externos)

---

## 1. Introduccion

### Proposito

El **Microscopy-Program** es un software de control de instrumentos de laboratorio basado en Python, disenado para operar un microscopio fototermico. Fue desarrollado en el *Laboratorio de Haces Dirigidos*, Facultad de Ingenieria, Universidad de Buenos Aires, por Facundo Zaldivar Escola.

### Que Hace el Software

La aplicacion coordina multiples instrumentos de laboratorio para realizar experimentos automatizados de microscopia fototermica:

- **Escaneo de Muestras**: Controla platinas de traslacion motorizadas (ejes X, Y, Z)
- **Generacion de Senales**: Controla generadores de funciones para barridos de frecuencia
- **Medicion de Senales**: Lee datos del amplificador lock-in para mediciones de precision
- **Captura de Imagenes**: Captura y muestra imagenes de camara para posicionamiento de muestras
- **Control de Temperatura**: Gestiona experimentos de calentamiento con hornos de temperatura controlada
- **Control de Foco**: Monitorea y ajusta el foco usando retroalimentacion laser y placa DAQ

### Flujo de Trabajo de Alto Nivel

```
1. Seleccion de Dispositivos  -> Seleccionar que instrumentos usar (reales o virtuales)
2. Configuracion              -> Establecer parametros para cada dispositivo
3. Ejecutar Experimento       -> Ejecutar con monitoreo en tiempo real
4. Exportar Datos             -> Guardar resultados en formato CSV o MATLAB
```

---

## 2. Descripcion General de la Arquitectura

### Filosofia de Diseno

El codigo sigue una **Arquitectura Basada en Componentes** utilizando el framework SER (Scientific Experiment Runner). Cada dispositivo de hardware esta encapsulado en una clase `Component` que proporciona:

1. **Instrument**: Logica del backend implementando interfaces SER
2. **Driver**: Capa de comunicacion con el hardware (basada en Lantz)
3. **UI de Configuracion**: Widgets PyQt5 para configuracion de parametros
4. **UI de Ejecucion** (opcional): Visualizacion en tiempo real durante experimentos

### Diagrama de Arquitectura de Componentes

```
┌────────────────────────────────────────────────────────────┐
│                         MainWindow                         │
│  ┌────────────────────────────────────────────────────────┐│
│  │              Pagina de Seleccion de Dispositivos       ││
│  │  [FunGen ▼] [Lockin ▼] [Motor X ▼] [Camara ▼] [Horno ▼]││
│  └────────────────────────────────────────────────────────┘│
│                              │                             │
│                              ▼                             │
│  ┌────────────────────────────────────────────────────────┐│
│  │              Framework SER (get_main_widget)           ││
│  │  ┌────────────────────────────────────────────────────┐││
│  │  │  Tab Configuracion  │  Tab Ejecucion  │  Tab Datos │││
│  │  └────────────────────────────────────────────────────┘││
│  │                                                        ││
│  │  ┌────────────────────────────────────────────────────┐││
│  │  │              Instancias de Componentes             │││
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │││
│  │  │  │ FunGen  │ │ Lockin  │ │ Platina │ │  Horno  │   │││
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │││
│  │  └────────────────────────────────────────────────────┘││
│  └────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────┘
```

### Estructura Interna de un Componente

```
Component
├── instrument: ConfigurableInstrument | ObservableInstrument
│   ├── driver: Driver Lantz (envuelto con lantz.qt)
│   ├── configure(*args) -> Dict
│   ├── get_points() -> Generator
│   └── point_amount() -> int
├── conf_ui: ConfigurationUI
│   ├── gui: Ruta al archivo .ui
│   └── backend: Referencia al instrumento
└── run_ui (opcional): ProcessDataUI
    └── add_data(data): Actualizar visualizacion
```

---

## 3. Estructura del Proyecto

```
Microscopy-Program/
├── main.py                        # Punto de entrada de la aplicacion
├── debug_main.py                  # Entrada para depuracion/pruebas
├── view_data.py                   # Utilidad para ver datos exportados
├── requirements.txt               # Dependencias de Python
├── frozenreqs.txt                 # Dependencias congeladas con versiones
├── devices.ini                    # Configuracion de dispositivos en tiempo de ejecucion (auto-generado)
│
├── UI/                            # Ventana principal e interfaz a nivel de aplicacion
│   ├── main_window.py             # Clase MainWindow - seleccion e inicializacion de dispositivos
│   └── main_window.ui             # Archivo UI de Qt Designer
│
├── components/                    # Componentes de hardware y modulos de UI
│   ├── __init__.py
│   ├── HP33120AFunGen/            # Componente Generador de Funciones
│   │   ├── __init__.py            # Clase del componente HPFunGen
│   │   ├── hp33120A_fungen.py     # Driver HP 33120A + VirtualFungen
│   │   ├── RigolAdapter.py        # Adaptador para Rigol DG1022
│   │   ├── dll_wrapper.py         # Wrapper USB FTDI para Prologix GPIB
│   │   ├── instrument_ui.py       # FunGenInstrument + FunGenConfUi
│   │   └── conf_ui.ui             # Archivo UI de Qt Designer
│   │
│   ├── Lockin/                    # Componente Amplificador Lock-in
│   │   ├── __init__.py            # Clase del componente AnfatecLockin
│   │   ├── anfatec_driver.py      # Driver Anfatec AMU 2.4 + VirtualLockin
│   │   ├── LI5655.py              # Driver NF LI5655/LI5660
│   │   ├── instrument_ui.py       # LockinInstrument + LockinUI + LockinGraphs
│   │   ├── conf.ui                # UI de configuracion
│   │   ├── graphs.ui              # Dialogo de graficos en tiempo real
│   │   └── demo.txt               # Archivo de datos demo
│   │
│   ├── Platina/                   # Componente Platina de Traslacion (motor)
│   │   ├── __init__.py            # Clase PlatinaComponent
│   │   ├── motor.py               # Driver de motor usando libximc
│   │   ├── instrument_ui.py       # PlatinaInstrument + PlatinaUI
│   │   ├── motor_test.py          # Utilidades de prueba del motor
│   │   ├── conf.ui                # UI de configuracion
│   │   └── *.cfg                  # Archivos de configuracion del motor
│   │
│   ├── CameraPlatina/             # Integracion Camara + Platina
│   │   ├── __init__.py            # Clase CameraPlatinaComponent
│   │   ├── camera.py              # CameraBackend, VirtualCamera, LucamCam
│   │   ├── instrument_ui.py       # CameraPlatinaInstrument + UIs
│   │   ├── calibration.py         # CalibrationUI para calibracion pixel-a-distancia
│   │   ├── custom_image.py        # ImageWidget para imagenes clickeables
│   │   ├── conf.ui                # UI de configuracion
│   │   ├── calibration.ui         # Dialogo de calibracion UI
│   │   └── camera_calibration.npy # Datos de calibracion almacenados
│   │
│   ├── Oven/                      # Componente Control de Temperatura
│   │   ├── __init__.py            # Clase del componente LinkamOven
│   │   ├── TMS94.py               # Driver Linkam TMS94 + VirtualOven
│   │   ├── instrument_ui.py       # OvenInstrument + OvenUI
│   │   └── conf.ui                # UI de configuracion
│   │
│   ├── USBDAQ/                    # Componente placa DAQ (control de foco)
│   │   ├── __init__.py            # Clase del componente USB2527DAC
│   │   ├── USB2527.py             # Driver MCC USB-2527 + VirtualDAC
│   │   ├── instrument_ui.py       # DACInstrument + DACUI + DACGraphs
│   │   ├── conf.ui                # UI de configuracion
│   │   └── graphs.ui              # Dialogo de graficos en tiempo real
│   │
│   ├── LinePlotter/               # Visualizacion de graficos de linea
│   ├── BarPlotter/                # Visualizacion de barras/histogramas
│   └── ScatterPlotter/            # Visualizacion de graficos de dispersion
│
├── Documentation/                 # Capturas de pantalla para documentacion
│
├── preprod/                       # Codigo de pre-produccion/pruebas
│
└── demo/                          # Archivos de configuracion demo
    └── run_conf.json              # Configuracion de experimento de ejemplo
```

---

## 4. Stack Tecnologico

### Tecnologias Principales

| Tecnologia | Version | Proposito |
|------------|---------|-----------|
| **Python** | 3.11.4+ | Lenguaje de programacion principal |
| **PyQt5** | 5.15+ | Framework de interfaz grafica |
| **Lantz** | git | Framework de abstraccion de drivers de hardware |
| **SER** | git | Framework para ejecucion de experimentos cientificos |
| **pyqtgraph** | 0.13.7 | Graficos en tiempo real |
| **OpenCV** | 4.10+ | Procesamiento de camara/imagenes |
| **NumPy** | 1.26+ | Computaciones numericas |
| **Pandas** | 2.2+ | Manipulacion de datos |
| **PyVISA** | 1.14+ | Comunicacion con instrumentos VISA |

### Bibliotecas Externas de Hardware

| Biblioteca | Proposito | Instalacion |
|------------|-----------|-------------|
| **libximc** | Interfaz del controlador de motores Standa | pip (incluido en requirements) |
| **lucam** | SDK de camara Lumenera | pip (incluido en requirements) |
| **mcculw** | DAQ de Measurement Computing | pip (incluido en requirements) |
| **Lockin.dll** | Amplificador lock-in Anfatec | Instalacion manual en `components/Lockin/` |

### Dependencias Principales de requirements.txt

```
opencv-python          # Procesamiento de camara e imagenes
keyboard               # Entrada de teclado para control de motor
libximc                # Controlador de motores Standa
lucam                  # SDK de camara Lumenera
pillow                 # Procesamiento de imagenes
matplotlib             # Graficos auxiliares
mcculw                 # Biblioteca DAQ de MCC
pyqtgraph              # Graficos en tiempo real
SER @ git+https://github.com/FranciscoGauna/SER.git
lantz.drivers @ git+https://github.com/lantzproject/lantz-drivers.git
PyVISA-py              # Comunicacion con instrumentos VISA
```

---

## 5. Frameworks Principales

### Framework SER

El framework SER (Scientific Experiment Runner) proporciona la infraestructura para la secuenciacion de experimentos. Gestiona:

- Generacion y disposicion de UI de configuracion
- Bucle de ejecucion de experimentos
- Recoleccion y agregacion de datos
- Visualizacion y exportacion de resultados

**Interfaces Principales de SER:**

```python
from SER.interfaces import (
    Component,                 # Clase base para componentes de hardware
    ComponentInitialization,   # Envoltorio con informacion de posicion/nombre
    ConfigurableInstrument,    # Dispositivos que se configuran antes de la medicion
    ObservableInstrument,      # Dispositivos que observan/miden datos
    ConfigurationUI,           # Widgets de UI para configuracion
    ProcessDataUI,             # Visualizacion de datos en tiempo real
    FinalDataUI,               # Visualizacion de datos finales
)
from SER import get_main_widget  # Crea la UI principal del experimento
```

**Detalles de las Interfaces:**

1. **ConfigurableInstrument**: Para dispositivos que necesitan configuracion antes de cada punto de medicion
   ```python
   class MiInstrumento(ConfigurableInstrument):
       def configure(self, *args) -> Dict[str, Any]:
           """Ejecutar configuracion y devolver resultados"""
           pass

       def get_points(self) -> Generator:
           """Generar puntos de configuracion"""
           pass

       def point_amount(self) -> int:
           """Devolver cantidad total de puntos"""
           pass
   ```

2. **ObservableInstrument**: Para dispositivos que miden/observan datos
   ```python
   class MiObservador(ObservableInstrument):
       def observe(self) -> Dict[str, Any]:
           """Tomar una medicion y devolver resultados"""
           pass
   ```

3. **ConfigurationUI**: Para widgets de configuracion de dispositivos
   ```python
   class MiConfigUI(ConfigurationUI):
       gui = "ruta/al/archivo_ui.ui"

       def __init__(self, backend):
           super().__init__(backend=backend)
   ```

### Framework Lantz

Lantz proporciona abstraccion de drivers de hardware con integracion Qt. Caracteristicas principales:

- **Feats**: Accesores tipo propiedad para parametros del hardware
- **Envoltorio Qt**: Integracion con GUI segura para hilos
- **Unidades**: Manejo de unidades fisicas

**Componentes Principales de Lantz:**

```python
from lantz import Driver, Feat
from lantz.qt import wrap_driver_cls
from lantz.qt.connect import connect_feat
```

**Ejemplo de Driver:**

```python
from lantz import Driver, Feat

class MiDriverHardware(Driver):
    @Feat(units="Hz", limits=(0, 100000))
    def frequency(self):
        """Leer frecuencia actual del hardware"""
        return self._query_frequency()

    @frequency.setter
    def frequency(self, value):
        """Establecer frecuencia en el hardware"""
        self._send_frequency_command(value)
```

---

## 6. Sistema de Componentes

### Estructura de un Componente

Todo componente de hardware sigue este patron:

```python
from SER.interfaces import Component
from lantz.qt import wrap_driver_cls

class MiComponente(Component):
    """Componente que envuelve un dispositivo de hardware"""

    @classmethod
    def virtual(cls):
        """Metodo de fabrica para modo virtual/pruebas"""
        driver = wrap_driver_cls(DriverVirtual)()
        self = cls()
        self.instrument = MiInstrumento(driver)
        self.conf_ui = MiConfigUI(self.instrument)
        return self

    @classmethod
    def real(cls, *args_conexion):
        """Metodo de fabrica para hardware real"""
        driver = wrap_driver_cls(DriverReal)(*args_conexion)
        self = cls()
        self.instrument = MiInstrumento(driver)
        self.conf_ui = MiConfigUI(self.instrument)
        return self

    def close_component(self):
        """Limpieza cuando el componente se cierra"""
        if hasattr(self, 'driver'):
            self.driver.finalize()
```

### ComponentInitialization

La clase `ComponentInitialization` envuelve componentes con metadatos para el framework SER:

```python
from SER.interfaces import ComponentInitialization

# Parametros: componente, prioridad_posicion, fila, columna, nombre
fungen_init = ComponentInitialization(
    component=fungen_comp,    # La instancia del Component
    position_priority=0,      # Prioridad de orden de ejecucion
    row=0,                    # Fila en la grilla de la UI de configuracion
    column=1,                 # Columna en la grilla de la UI de configuracion
    name="Fungen 1"           # Nombre para mostrar (tambien usado como prefijo de clave de datos)
)
```

### Registro de Componentes

Los componentes se registran en `UI/main_window.py`:

```python
class MainWindow(QMainWindow):
    def load_options(self):
        # Definir metodos de fabrica para cada opcion de dispositivo
        self.fungen_ops = {
            "Virtual": HPFunGen.virtual,
            "HP 33120A": lambda: HPFunGen.via_prologix_gpib(addr),
            "Rigol DG1022": HPFunGen.rigol
        }
        self.fungen_cb.addItems(self.fungen_ops.keys())

        # ... similar para otros componentes

    def switch_window(self):
        # Crear componentes basados en la seleccion del usuario
        self.fungen_comp = self.fungen_ops[self.fungen_cb.currentText()]()
        fungen_init = ComponentInitialization(self.fungen_comp, 0, 0, 1, "Fungen 1")

        # Pasar al framework SER
        ser_widget = get_main_widget(
            configurable=[fungen_init, platina_init, oven_init],
            observable=[lockin_init, dac_init],
            process_data_uis=[...],
            final_data_uis=[...],
        )
```

---

## 7. Referencia de Componentes de Hardware

### 7.1 HP33120AFunGen (Generador de Funciones)

**Ubicacion:** `components/HP33120AFunGen/`

**Dispositivos Soportados:**
- HP 33120A (mediante adaptador Prologix GPIB)
- Rigol DG1022 (mediante USB)
- Virtual (para pruebas)

**Archivos Principales:**
| Archivo | Proposito |
|---------|-----------|
| `__init__.py` | Clase del componente `HPFunGen` con metodos de fabrica |
| `hp33120A_fungen.py` | Driver HP 33120A + `VirtualFungen` |
| `RigolAdapter.py` | Adaptador para Rigol DG1022 para coincidir con la interfaz HP |
| `dll_wrapper.py` | Wrapper USB FTDI para adaptador Prologix GPIB |
| `instrument_ui.py` | `FunGenInstrument` + `FunGenConfUi` |

**Parametros Configurables:**
- Tipo de forma de onda (SIN, SQU, TRI, RAMP, NOIS, DC, USER)
- Rango de frecuencia (barrido lineal o logaritmico)
- Amplitud y offset DC

### 7.2 Lockin (Amplificador Lock-in)

**Ubicacion:** `components/Lockin/`

**Dispositivos Soportados:**
- Anfatec AMU 2.4 (mediante DLL)
- NF LI5655/LI5660 (mediante VISA/USB)
- Virtual/Demo (para pruebas)

**Archivos Principales:**
| Archivo | Proposito |
|---------|-----------|
| `__init__.py` | Clase del componente `AnfatecLockin` |
| `anfatec_driver.py` | Driver Anfatec + `VirtualLockin` + `DemoLockin` |
| `LI5655.py` | Driver NF LI5655/LI5660 |
| `instrument_ui.py` | `LockinInstrument` + `LockinUI` + `LockinGraphs` |

**Salidas Observables:**
- Amplitud (V)
- Fase (grados)
- Graficos de monitoreo en tiempo real

### 7.3 Platina (Platina de Traslacion)

**Ubicacion:** `components/Platina/`

**Dispositivos Soportados:**
- Cualquier motor compatible con XIMC de Standa
- Virtual (motor emulado)

**Archivos Principales:**
| Archivo | Proposito |
|---------|-----------|
| `__init__.py` | Clase `PlatinaComponent` |
| `motor.py` | Clase `Motor` usando libximc, `get_available_motors()` |
| `instrument_ui.py` | `PlatinaInstrument` + `PlatinaUI` |
| `*.cfg` | Archivos de configuracion de motor (formato XIMC) |

**Caracteristicas:**
- Movimiento sincrono y asincrono
- Retroalimentacion de posicion con soporte de encoder
- Compensacion de backlash
- Control de velocidad/aceleracion
- Movimiento jog controlado por teclado

### 7.4 CameraPlatina (Integracion Camara + Platina)

**Ubicacion:** `components/CameraPlatina/`

**Camaras Soportadas:**
- Lumenera Infinity 1 (mediante SDK lucam)
- Cualquier webcam compatible con OpenCV
- Virtual (para pruebas)

**Archivos Principales:**
| Archivo | Proposito |
|---------|-----------|
| `__init__.py` | Clase `CameraPlatinaComponent` |
| `camera.py` | `CameraBackend`, `VirtualCamera`, `LucamCam` |
| `instrument_ui.py` | `CameraPlatinaInstrument` + clases de UI |
| `calibration.py` | `CalibrationUI` para calibracion pixel-a-distancia |
| `custom_image.py` | `ImageWidget` para visualizacion de imagenes clickeables |

**Caracteristicas:**
- Vista previa de camara en vivo
- Click para definir trayectoria de escaneo
- Calibracion pixel-a-motor
- Modos de escaneo cuadrado (grilla) o lineal

### 7.5 Oven (Control de Temperatura)

**Ubicacion:** `components/Oven/`

**Dispositivos Soportados:**
- Linkam TMS 94 (mediante serial)
- Virtual (para pruebas)

**Archivos Principales:**
| Archivo | Proposito |
|---------|-----------|
| `__init__.py` | Clase del componente `LinkamOven` |
| `TMS94.py` | Driver `LinkamTMS94` + `VirtualOven` |
| `instrument_ui.py` | `OvenInstrument` + `OvenUI` |

**Parametros Configurables:**
- Rango de temperatura
- Velocidad de calentamiento

### 7.6 USBDAQ (Placa DAQ / Control de Foco)

**Ubicacion:** `components/USBDAQ/`

**Dispositivos Soportados:**
- MCC USB-2527 (mediante mcculw)
- Virtual (para pruebas)

**Archivos Principales:**
| Archivo | Proposito |
|---------|-----------|
| `__init__.py` | Clase del componente `USB2527DAC` |
| `USB2527.py` | `USB2527Driver` + `VirtualDAC` |
| `instrument_ui.py` | `DACInstrument` + `DACUI` + `DACGraphs` + `DACStatus` |

**Caracteristicas:**
- Entrada/salida analogica
- E/S digital para control de laser
- Monitoreo de foco en tiempo real
- Senales de suma y error de foco del fotodiodo ABCD

### 7.7 Componentes de Visualizacion

**LinePlotter** (`components/LinePlotter/`):
- Graficos de linea/dispersion en tiempo real
- Implementa la interfaz `ProcessDataUI`

**BarPlotter** (`components/BarPlotter/`):
- Graficos de barras e histogramas
- Implementa las interfaces `ProcessDataUI` y `FinalDataUI`

---

## 8. Flujo de Datos y Ciclo de Vida de la Aplicacion

### Inicio de la Aplicacion

```
main.py
    │
    ├── Crear QApplication
    ├── Inicializar logging
    │
    └── MainWindow.__init__()
            │
            ├── Cargar UI desde main_window.ui
            ├── load_options()  # Poblar ComboBoxes de dispositivos
            └── show()
```

### Flujo de Inicializacion de Dispositivos

```
El usuario hace click en el boton "Lanzar"
    │
    └── MainWindow.switch_window()
            │
            ├── Para cada tipo de dispositivo:
            │   │
            │   ├── Obtener metodo de fabrica del diccionario ops
            │   │   fungen_ops[combobox.currentText()]()
            │   │
            │   ├── La fabrica crea el driver
            │   │   driver = wrap_driver_cls(ClaseDriver)()
            │   │
            │   ├── La fabrica crea el componente
            │   │   component.instrument = Instrumento(driver)
            │   │   component.conf_ui = ConfigUI(instrumento)
            │   │
            │   └── Envolver en ComponentInitialization
            │       ComponentInitialization(component, prioridad, fila, col, nombre)
            │
            ├── Crear componentes de visualizacion
            │   LinePlotter, BarPlotter, etc.
            │
            └── Llamar a SER.get_main_widget()
                    │
                    ├── configurable_components
                    ├── observable_components
                    ├── process_data_uis
                    └── final_data_uis
```

### Flujo de Ejecucion del Experimento

```
El usuario hace click en "Ejecutar" en el widget SER
    │
    └── Bucle de Ejecucion del Framework SER
            │
            ├── Para cada punto de configuracion:
            │   │
            │   ├── Llamar configurable.configure(*punto)
            │   │   └── Devuelve Dict con datos de configuracion
            │   │
            │   ├── Esperar estabilizacion (si esta configurado)
            │   │
            │   ├── Llamar observable.observe()
            │   │   └── Devuelve Dict con datos de medicion
            │   │
            │   ├── Agregar datos de todos los componentes
            │   │
            │   ├── Llamar process_ui.add_data(datos)
            │   │   └── Actualizar visualizaciones en tiempo real
            │   │
            │   └── Almacenar fila de datos
            │
            └── Al completarse:
                    │
                    ├── Llamar final_ui.set_data(todos_los_datos)
                    └── Habilitar exportacion de datos
```

### Formato de Salida de Datos

Los datos del experimento se recolectan como diccionarios y se exportan como CSV:

```csv
time,Platina_motor_x_position,Platina_motor_y_position,Fungen 1_frequency,Lockin_amplitude,Lockin_phase,...
0.0,0.0,0.0,100.0,0.00123,45.2,...
0.5,1.0,0.0,200.0,0.00098,42.1,...
```

Los nombres de columna se generan a partir de: `{nombre_componente}_{nombre_variable}`

---

## 9. Modelo de Hilos

La aplicacion utiliza multiples hilos para una UI responsiva:

### Vista General de Hilos

```
┌─────────────────────────────────────────────────────────────────┐
│                        Hilo Principal                            │
│                    Bucle de Eventos PyQt5                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Actualizaciones de UI, Entrada del Usuario, Senales/Slots  ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
           │
           ├──────────────────────────────────────────────────────┐
           │                                                      │
┌──────────▼──────────┐  ┌───────────────────┐  ┌────────────────▼────────┐
│  Hilo de Estado     │  │  Hilo de Camara   │  │  Hilo de Estado DAC     │
│  del Motor          │  │                   │  │                         │
│  (Motor.MotorStatus)│  │  (CameraPlatinaUI)│  │  (DACStatus)            │
│                     │  │                   │  │                         │
│  Consulta posicion  │  │  Captura cuadros  │  │  Lee entradas analogicas│
│  del motor @ 100Hz  │  │  continuamente    │  │  continuamente          │
└─────────────────────┘  └───────────────────┘  └─────────────────────────┘
           │
           └──────────────────────────────────────────────────────┐
                                                                  │
┌─────────────────────────────────────────────────────────────────▼───────┐
│                       Hilo de Graficos Lockin                           │
│                       (LockinGraphs)                                    │
│                                                                         │
│  Monitoreo continuo del lock-in para visualizacion                     │
│  de amplitud/fase en tiempo real                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### Patron de Actualizaciones de Estado Seguras para Hilos

```python
from threading import Thread
from time import sleep

class MonitorDeEstado:
    def __init__(self):
        self.running = True
        self.thread = Thread(target=self._bucle_actualizacion, daemon=True)
        self.thread.start()

    def _bucle_actualizacion(self):
        while self.running:
            self._leer_y_actualizar_estado()
            sleep(0.01)  # Consulta a 100 Hz

    def stop(self):
        self.running = False
        self.thread.join(timeout=1.0)
```

### Senales/Slots de Qt para Actualizaciones de UI Seguras entre Hilos

Cuando se actualiza la UI desde hilos en segundo plano, usar senales de Qt:

```python
from PyQt5.QtCore import pyqtSignal, QObject

class EmisorDeDatos(QObject):
    datos_listos = pyqtSignal(dict)

class TrabajadorEnSegundoPlano:
    def __init__(self, widget_ui):
        self.emisor = EmisorDeDatos()
        self.emisor.datos_listos.connect(widget_ui.actualizar_visualizacion)

    def _hilo_trabajador(self):
        while self.running:
            datos = self._leer_hardware()
            self.emisor.datos_listos.emit(datos)  # Actualizacion de UI segura entre hilos
```

---

## 10. Agregar Nuevos Componentes

### Guia Paso a Paso

#### Paso 1: Crear Directorio del Componente

```bash
mkdir components/NuevoDispositivo
touch components/NuevoDispositivo/__init__.py
touch components/NuevoDispositivo/driver.py
touch components/NuevoDispositivo/instrument_ui.py
```

#### Paso 2: Crear el Driver

`components/NuevoDispositivo/driver.py`:

```python
from lantz import Driver, Feat, Action

class NuevoDispositivoDriver(Driver):
    """Driver para hardware real"""

    def __init__(self, *args_conexion):
        super().__init__()
        # Inicializar conexion

    def initialize(self):
        """Se llama cuando el driver se abre"""
        pass

    def finalize(self):
        """Se llama cuando el driver se cierra"""
        pass

    @Feat(units="Hz", limits=(0, 100000))
    def frequency(self):
        """Obtener frecuencia actual"""
        return self._query("FREQ?")

    @frequency.setter
    def frequency(self, value):
        """Establecer frecuencia"""
        self._send(f"FREQ {value}")

    @Action()
    def reset(self):
        """Restablecer dispositivo a valores por defecto"""
        self._send("*RST")


class NuevoDispositivoVirtual(Driver):
    """Driver virtual para pruebas sin hardware"""

    def __init__(self):
        super().__init__()
        self._frequency = 1000.0

    @Feat(units="Hz", limits=(0, 100000))
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self._frequency = value
```

#### Paso 3: Crear Instrumento y UI de Configuracion

`components/NuevoDispositivo/instrument_ui.py`:

```python
from typing import Dict, Any, Generator
from SER.interfaces import ConfigurableInstrument, ConfigurationUI
from lantz.qt.connect import connect_feat
import numpy as np

class NuevoDispositivoInstrument(ConfigurableInstrument):
    """Logica del instrumento que envuelve el driver"""

    def __init__(self, driver):
        self.driver = driver
        self._freq_inicio = 100
        self._freq_fin = 10000
        self._pasos = 10
        self._escala_log = True

    def configure(self, frecuencia) -> Dict[str, Any]:
        """Configurar dispositivo para punto de medicion"""
        self.driver.frequency = frecuencia
        return {"frequency": frecuencia}

    def get_points(self) -> Generator:
        """Generar puntos de configuracion"""
        if self._escala_log:
            freqs = np.logspace(
                np.log10(self._freq_inicio),
                np.log10(self._freq_fin),
                self._pasos
            )
        else:
            freqs = np.linspace(self._freq_inicio, self._freq_fin, self._pasos)

        for freq in freqs:
            yield (freq,)

    def point_amount(self) -> int:
        """Devolver cantidad total de puntos"""
        return self._pasos

    def get_config(self) -> Dict[str, Any]:
        """Exportar configuracion actual"""
        return {
            "freq_inicio": self._freq_inicio,
            "freq_fin": self._freq_fin,
            "pasos": self._pasos,
            "escala_log": self._escala_log,
        }

    def set_config(self, config: Dict[str, Any]):
        """Importar configuracion"""
        self._freq_inicio = config.get("freq_inicio", self._freq_inicio)
        self._freq_fin = config.get("freq_fin", self._freq_fin)
        self._pasos = config.get("pasos", self._pasos)
        self._escala_log = config.get("escala_log", self._escala_log)


class NuevoDispositivoUI(ConfigurationUI):
    """Widget de UI de configuracion"""

    gui = "conf.ui"  # Ruta al archivo .ui de Qt Designer

    def __init__(self, backend: NuevoDispositivoInstrument):
        super().__init__(backend=backend)

        # Conectar widgets de UI a propiedades del instrumento
        # Asumiendo que conf.ui tiene spinboxes: start_freq_spin, end_freq_spin, steps_spin
        # y un checkbox: log_scale_check

        self.widget.start_freq_spin.valueChanged.connect(
            lambda v: setattr(self.backend, '_freq_inicio', v)
        )
        self.widget.end_freq_spin.valueChanged.connect(
            lambda v: setattr(self.backend, '_freq_fin', v)
        )
        self.widget.steps_spin.valueChanged.connect(
            lambda v: setattr(self.backend, '_pasos', v)
        )
        self.widget.log_scale_check.toggled.connect(
            lambda v: setattr(self.backend, '_escala_log', v)
        )

        # Si se conecta a Feats de Lantz en el driver:
        # connect_feat(self.widget.freq_spin, self.backend.driver, "frequency")
```

#### Paso 4: Crear la Clase del Componente

`components/NuevoDispositivo/__init__.py`:

```python
from SER.interfaces import Component
from lantz.qt import wrap_driver_cls
from .driver import NuevoDispositivoDriver, NuevoDispositivoVirtual
from .instrument_ui import NuevoDispositivoInstrument, NuevoDispositivoUI

class NuevoDispositivoComponent(Component):
    """Componente para hardware NuevoDispositivo"""

    @classmethod
    def virtual(cls):
        """Crear componente con driver virtual (para pruebas)"""
        driver = wrap_driver_cls(NuevoDispositivoVirtual)()
        self = cls()
        self.instrument = NuevoDispositivoInstrument(driver)
        self.conf_ui = NuevoDispositivoUI(self.instrument)
        return self

    @classmethod
    def real(cls, puerto: str):
        """Crear componente con hardware real"""
        driver = wrap_driver_cls(NuevoDispositivoDriver)(puerto)
        driver.initialize()
        self = cls()
        self.driver = driver  # Almacenar para limpieza
        self.instrument = NuevoDispositivoInstrument(driver)
        self.conf_ui = NuevoDispositivoUI(self.instrument)
        return self

    def close_component(self):
        """Limpieza cuando el componente se cierra"""
        if hasattr(self, 'driver'):
            self.driver.finalize()
```

#### Paso 5: Crear el Archivo UI

Usar Qt Designer para crear `components/NuevoDispositivo/conf.ui` con los widgets apropiados.

Alternativamente, crear programaticamente:

```python
# En instrument_ui.py, sobreescribir gui con None y construir UI en __init__
class NuevoDispositivoUI(ConfigurationUI):
    gui = None

    def __init__(self, backend):
        super().__init__(backend=backend)

        from PyQt5.QtWidgets import QVBoxLayout, QSpinBox, QLabel, QCheckBox

        layout = QVBoxLayout()

        self.start_freq_spin = QSpinBox()
        self.start_freq_spin.setRange(1, 100000)
        layout.addWidget(QLabel("Frecuencia Inicial (Hz)"))
        layout.addWidget(self.start_freq_spin)

        # ... agregar mas widgets

        self.widget.setLayout(layout)
```

#### Paso 6: Registrar en MainWindow

Editar `UI/main_window.py`:

```python
from components.NuevoDispositivo import NuevoDispositivoComponent

class MainWindow(QMainWindow):
    def load_options(self):
        # ... codigo existente ...

        self.nuevo_disp_ops = {
            "Virtual": NuevoDispositivoComponent.virtual,
            "Real": lambda: NuevoDispositivoComponent.real("COM3"),
        }
        self.nuevo_disp_cb.addItems(self.nuevo_disp_ops.keys())

    def switch_window(self):
        # ... codigo existente ...

        self.nuevo_disp_comp = self.nuevo_disp_ops[self.nuevo_disp_cb.currentText()]()
        nuevo_disp_init = ComponentInitialization(
            self.nuevo_disp_comp,
            position_priority=0,  # Ajustar segun sea necesario
            row=0,
            column=2,  # Ajustar posicion en la grilla
            name="NuevoDispositivo"
        )

        # Agregar a la lista configurable u observable
        ser_widget = get_main_widget(
            configurable=[..., nuevo_disp_init],
            # o observable=[..., nuevo_disp_init],
            ...
        )
```

#### Paso 7: Actualizar main_window.ui

Agregar un ComboBox y Label para el nuevo dispositivo en Qt Designer, o agregar programaticamente.

---

## 11. Sistema de Configuracion

### Configuracion en Tiempo de Ejecucion (devices.ini)

El archivo `devices.ini` almacena parametros de conexion para dispositivos de hardware. Se auto-genera en la primera ejecucion con valores por defecto.

**Ubicacion:** Mismo directorio que `main.py`

**Formato:**
```ini
[HP33120AFungen]
PROLOGIX ADDR = 10

[Web Cam]
Index = 0

[Linkam TMS 94]
Port = 15

[USB2527DAC]
Board Num = 0
```

**Como funciona en el codigo:**

```python
# UI/main_window.py
from configparser import ConfigParser

config = ConfigParser()

# Valores por defecto
config["HP33120AFungen"] = {"PROLOGIX ADDR": "10"}
config["Web Cam"] = {"Index": "0"}
# ...

# Cargar o crear archivo
if path.exists("devices.ini"):
    config.read("devices.ini")
else:
    with open("devices.ini", "w") as f:
        config.write(f)

# Usar en metodos de fabrica
lambda: HPFunGen.via_prologix_gpib(int(config["HP33120AFungen"]["PROLOGIX ADDR"]))
```

### Agregar Nuevas Opciones de Configuracion

1. Agregar valor por defecto en `MainWindow`:
   ```python
   config["NuevoDispositivo"] = {"Port": "COM3", "Baudrate": "9600"}
   ```

2. Usar en metodo de fabrica:
   ```python
   self.nuevo_disp_ops = {
       "Real": lambda: NuevoDispositivoComponent.real(
           config["NuevoDispositivo"]["Port"],
           int(config["NuevoDispositivo"]["Baudrate"])
       ),
   }
   ```

### Configuracion de Experimento (JSON)

Los parametros de experimento se pueden guardar/cargar como JSON:

```python
# Guardar configuracion
config_dict = {}
for component in components:
    config_dict[component.name] = component.instrument.get_config()

with open("config_experimento.json", "w") as f:
    json.dump(config_dict, f, indent=2)

# Cargar configuracion
with open("config_experimento.json", "r") as f:
    config_dict = json.load(f)

for component in components:
    if component.name in config_dict:
        component.instrument.set_config(config_dict[component.name])
```

### Archivos de Configuracion de Motor (.cfg)

Los archivos de configuracion de motor estan en formato XIMC y se ubican en `components/Platina/`:

| Archivo | Motor |
|---------|-------|
| `8MT173-10.cfg` | Standa 8MT173-10 |
| `8MT173-10-Encoder.cfg` | Mismo con encoder |
| `8MTF-75LS05-Encoder-x.cfg` | Eje X con encoder |
| `8MTF-75LS05-Encoder-y.cfg` | Eje Y con encoder |
| `flash_eje_x.cfg` | Platina flash eje X |
| `flash_eje_y.cfg` | Platina flash eje Y |

---

## 12. Pruebas y Desarrollo

### Ejecucion en Modo Virtual

Todos los componentes soportan modo "Virtual" para pruebas sin hardware:

```bash
python main.py
# Seleccionar "Virtual" para todos los desplegables de dispositivos
# Hacer click en "Lanzar"
```

### Configuracion Demo

Cargar configuracion demo desde `demo/run_conf.json`:

```python
# En el widget SER, usar la funcion de cargar configuracion
# para importar demo/run_conf.json
```

### Pruebas de Componentes

Las pruebas individuales de componentes se pueden ejecutar desde `preprod/` o los directorios de componentes:

```bash
# Probar motor
python -m components.Platina.motor_test

# Probar lock-in
python preprod/lockin.py

# Probar camara
python preprod/camera.py
```

### Punto de Entrada de Depuracion

Usar `debug_main.py` para pruebas de desarrollo:

```bash
python debug_main.py
```

### Crear Datos de Prueba

Para `DemoLockin`, los datos se cargan desde `components/Lockin/demo.txt`:

```
# formato de demo.txt (separado por tabulaciones)
amplitud   fase
0.001      45.2
0.002      42.1
...
```

### Logging

La aplicacion usa el sistema de logging de Lantz:

```python
from lantz.core.log import log_to_screen
from logging import DEBUG, INFO, WARNING, ERROR

# En main.py
log_to_screen(ERROR)  # Solo mostrar errores

# Para desarrollo, usar DEBUG
log_to_screen(DEBUG)
```

---

## 13. Patrones Comunes y Buenas Practicas

### Patron de Driver Lantz

```python
from lantz import Driver, Feat, Action

class MiDriver(Driver):
    @Feat(units="Hz", limits=(0, 100000))
    def frequency(self):
        return self._freq

    @frequency.setter
    def frequency(self, value):
        self._freq = value
        self._enviar_a_hardware(value)

    @Action()
    def reset(self):
        self._send("*RST")
```

### Patron de Carga de UI Qt

```python
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from os import path

class MiUI(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = path.join(
            path.dirname(path.realpath(__file__)),
            "mi_ui.ui"
        )
        uic.loadUi(ui_path, self)
```

### Patron de Conexion de Features

```python
from lantz.qt.connect import connect_feat

# Conecta un QSpinBox a un Feat de Lantz
connect_feat(self.widget.spinbox, self.driver, "frequency")
# Ahora los cambios en el spinbox actualizan automaticamente driver.frequency
# y los cambios en driver.frequency actualizan el spinbox
```

### Monitoreo de Estado Seguro entre Hilos

```python
from threading import Thread
from time import sleep

class MonitorDeEstado:
    def __init__(self):
        self.running = True
        self.thread = Thread(target=self._bucle_actualizacion, daemon=True)
        self.thread.start()

    def _bucle_actualizacion(self):
        while self.running:
            self._leer_estado()
            sleep(0.01)

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
```

### Emision de Senales para Datos en Tiempo Real

```python
from PyQt5.QtCore import pyqtSignal

class FuenteDeDatos(QObject):
    nuevos_datos = pyqtSignal(float, float)  # amplitud, fase

    def leer_datos(self):
        amp, fase = self.driver.read()
        self.nuevos_datos.emit(amp, fase)

# En la clase de UI
self.fuente_datos.nuevos_datos.connect(self.actualizar_grafico)
```

### Manejo de Errores en Drivers

```python
class MiDriver(Driver):
    @Feat
    def value(self):
        try:
            respuesta = self._query("VAL?")
            return float(respuesta)
        except (ValueError, TimeoutError) as e:
            self.log_error(f"Error al leer valor: {e}")
            raise
```

---

## 14. Solucion de Problemas de Desarrollo

### Errores de Importacion

**Problema:** `ModuleNotFoundError: No module named 'SER'`

**Solucion:**
```bash
pip install git+https://github.com/FranciscoGauna/SER.git
```

### Problemas de Conexion del Driver

**Problema:** El driver no puede conectarse al hardware

**Pasos de Depuracion:**
1. Probar el hardware con el software del fabricante primero
2. Verificar parametros de conexion (puerto, direccion, etc.)
3. Verificar instalacion del driver (revisar `pip list`)
4. Probar en modo virtual para aislar problemas de hardware
5. Agregar logging de depuracion:
   ```python
   from lantz.core.log import log_to_screen
   from logging import DEBUG
   log_to_screen(DEBUG)
   ```

### La UI No Se Actualiza desde un Hilo en Segundo Plano

**Problema:** La UI se congela o no se actualiza cuando el hardware cambia

**Solucion:** Usar senales de Qt para actualizaciones seguras entre hilos:
```python
# Incorrecto (se cuelga o congela)
def hilo_segundo_plano(self):
    while True:
        datos = self.leer_hardware()
        self.label.setText(str(datos))  # NO HACER ESTO

# Correcto
class Emisor(QObject):
    actualizar = pyqtSignal(str)

def hilo_segundo_plano(self):
    while True:
        datos = self.leer_hardware()
        self.emisor.actualizar.emit(str(datos))

# Conectar en __init__
self.emisor.actualizar.connect(self.label.setText)
```

### El Motor No Se Mueve

**Pasos de Depuracion:**
1. Verificar la instalacion del software XIMC
2. Verificar que el motor sea detectado: `get_available_motors()`
3. Comprobar que el archivo de configuracion coincida con el modelo del motor
4. Probar con motor_test.py

### La Camara Muestra Imagen Negra

**Pasos de Depuracion:**
1. Verificar el indice de la camara en `devices.ini`
2. Probar directamente con OpenCV:
   ```python
   import cv2
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   print(f"Exito: {ret}, Forma: {frame.shape if ret else 'N/A'}")
   ```
3. Verificar que ninguna otra aplicacion este usando la camara

### Archivo UI de PyQt No Carga

**Problema:** `uic.loadUi()` falla

**Solucion:**
- Verificar que la ruta del archivo .ui sea correcta
- Usar ruta absoluta:
  ```python
  ui_path = path.join(path.dirname(path.realpath(__file__)), "conf.ui")
  ```
- Comprobar que el archivo .ui no este corrupto (abrir en Qt Designer)

---

## 15. Recursos Externos

### Documentacion

| Recurso | URL |
|---------|-----|
| Framework SER | https://github.com/FranciscoGauna/SER |
| Documentacion de Lantz | https://lantz.readthedocs.io/ |
| Documentacion de Motores XIMC | https://files.xisupport.com/Software.en.html |
| Documentacion de PyQt5 | https://www.riverbankcomputing.com/static/Docs/PyQt5/ |
| Documentacion de pyqtgraph | https://pyqtgraph.readthedocs.io/ |

### Enlaces de Fabricantes de Hardware

| Dispositivo | Fabricante | Enlace |
|-------------|------------|--------|
| Lock-in AMU 2.4 | Anfatec | https://www.anfatec.de/ |
| Platinas de Traslacion | Standa | https://www.standa.lt/ |
| Camaras | Lumenera | https://www.lumenera.com/ |
| Placas DAQ | Digilent/MCC | https://www.mccdaq.com/ |
| Platinas Linkam | Linkam | https://www.linkam.co.uk/ |

### Herramientas de Desarrollo

| Herramienta | Proposito |
|-------------|-----------|
| Qt Designer | Diseno de layout de UI |
| NI MAX | Descubrimiento de dispositivos VISA |
| Anaconda | Gestion de entornos Python |

---

## Apendice A: Referencia Rapida

### Lista de Verificacion para Crear un Nuevo Componente

- [ ] Crear directorio `components/NuevoDispositivo/`
- [ ] Crear `driver.py` con drivers real y virtual
- [ ] Crear `instrument_ui.py` con clases de instrumento y UI
- [ ] Crear `__init__.py` con clase del componente y metodos de fabrica
- [ ] Crear `conf.ui` usando Qt Designer (opcional)
- [ ] Agregar a `UI/main_window.py`:
  - [ ] Importar componente
  - [ ] Agregar al diccionario ops en `load_options()`
  - [ ] Agregar items al ComboBox
  - [ ] Crear componente en `switch_window()`
  - [ ] Agregar a la llamada `get_main_widget()` de SER
- [ ] Actualizar `main_window.ui` con nuevo ComboBox (opcional)
- [ ] Agregar configuracion a los valores por defecto de `devices.ini`
- [ ] Probar en modo virtual
- [ ] Probar con hardware real

### Referencia Rapida de Interfaces SER

```python
# ConfigurableInstrument
configure(*args) -> Dict[str, Any]
get_points() -> Generator
point_amount() -> int

# ObservableInstrument
observe() -> Dict[str, Any]

# ConfigurationUI
gui: str  # Ruta al archivo .ui
backend: Instrument

# ProcessDataUI
add_data(data: Dict)

# FinalDataUI
set_data(data: List[Dict])

# ComponentInitialization
ComponentInitialization(component, priority, row, col, name)
```

### Referencia Rapida de Lantz

```python
from lantz import Driver, Feat, Action
from lantz.qt import wrap_driver_cls
from lantz.qt.connect import connect_feat

# Envolver driver para seguridad de hilos Qt
DriverEnvuelto = wrap_driver_cls(MiDriver)
driver = DriverEnvuelto()

# Conectar widget de UI a Feat
connect_feat(widget, driver, "nombre_feat")
```

---

*Este manual del desarrollador fue creado para el Microscopy-Program desarrollado por Facundo Zaldivar Escola en el Laboratorio de Haces Dirigidos, Facultad de Ingenieria, Universidad de Buenos Aires.*
