# Microscopy-Program Developer Manual

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architecture Overview](#2-architecture-overview)
3. [Project Structure](#3-project-structure)
4. [Technology Stack](#4-technology-stack)
5. [Core Frameworks](#5-core-frameworks)
6. [Component System](#6-component-system)
7. [Hardware Components Reference](#7-hardware-components-reference)
8. [Data Flow and Application Lifecycle](#8-data-flow-and-application-lifecycle)
9. [Threading Model](#9-threading-model)
10. [Adding New Components](#10-adding-new-components)
11. [Configuration System](#11-configuration-system)
12. [Testing and Development](#12-testing-and-development)
13. [Common Patterns and Best Practices](#13-common-patterns-and-best-practices)
14. [Troubleshooting Development Issues](#14-troubleshooting-development-issues)
15. [External Resources](#15-external-resources)

---

## 1. Introduction

### Purpose

The **Microscopy-Program** is Python-based laboratory instrument control software designed for operating a photothermal microscope. It was developed at the *Laboratorio de Haces Dirigidos*, Facultad de Ingenieria, Universidad de Buenos Aires by Facundo Zaldivar Escola.

### What the Software Does

The application coordinates multiple laboratory instruments to perform automated photothermal microscopy experiments:

- **Sample Scanning**: Controls motorized translation stages (X, Y, Z axes)
- **Signal Generation**: Controls function generators for frequency sweeps
- **Signal Measurement**: Reads lock-in amplifier data for precision measurements
- **Image Capture**: Captures and displays camera images for sample positioning
- **Temperature Control**: Manages heating experiments with temperature-controlled ovens
- **Focus Control**: Monitors and adjusts focus using laser feedback and DAQ board

### High-Level Workflow

```
1. Device Selection     -> Select which instruments to use (real or virtual)
2. Configuration        -> Set parameters for each device
3. Run Experiment       -> Execute with real-time monitoring
4. Export Data          -> Save results in CSV or MATLAB format
```

---

## 2. Architecture Overview

### Design Philosophy

The codebase follows a **Component-Based Architecture** using the SER (Scientific Experiment Runner) framework. Each hardware device is encapsulated in a `Component` class that provides:

1. **Instrument**: Backend logic implementing SER interfaces
2. **Driver**: Hardware communication layer (Lantz-based)
3. **Configuration UI**: PyQt5 widgets for parameter setup
4. **Run UI** (optional): Real-time visualization during experiments

### Component Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         MainWindow                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Device Selection Page                     ││
│  │  [FunGen ▼] [Lockin ▼] [Motor X ▼] [Camera ▼] [Oven ▼]     ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              SER Framework (get_main_widget)                 ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │  Configuration Tab  │  Run Tab  │  Data Tab             │││
│  │  └─────────────────────────────────────────────────────────┘││
│  │                                                              ││
│  │  ┌──────────────────────────────────────────────────────┐   ││
│  │  │              Component Instances                      │   ││
│  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │   ││
│  │  │  │ FunGen  │ │ Lockin  │ │ Platina │ │  Oven   │    │   ││
│  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │   ││
│  │  └──────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### Component Internal Structure

```
Component
├── instrument: ConfigurableInstrument | ObservableInstrument
│   ├── driver: Lantz Driver (wrapped with lantz.qt)
│   ├── configure(*args) -> Dict
│   ├── get_points() -> Generator
│   └── point_amount() -> int
├── conf_ui: ConfigurationUI
│   ├── gui: Path to .ui file
│   └── backend: Reference to instrument
└── run_ui (optional): ProcessDataUI
    └── add_data(data): Update visualization
```

---

## 3. Project Structure

```
Microscopy-Program/
├── main.py                        # Application entry point
├── debug_main.py                  # Debug/testing entry
├── view_data.py                   # Utility to view exported data
├── requirements.txt               # Python dependencies
├── frozenreqs.txt                 # Frozen dependencies with versions
├── devices.ini                    # Runtime device configuration (auto-generated)
│
├── UI/                            # Main window and application-level UI
│   ├── main_window.py             # MainWindow class - device selection and initialization
│   └── main_window.ui             # Qt Designer UI file
│
├── components/                    # Hardware components and UI modules
│   ├── __init__.py
│   ├── HP33120AFunGen/            # Function Generator component
│   │   ├── __init__.py            # HPFunGen component class
│   │   ├── hp33120A_fungen.py     # HP 33120A driver + VirtualFungen
│   │   ├── RigolAdapter.py        # Adapter for Rigol DG1022
│   │   ├── dll_wrapper.py         # FTDI USB wrapper for Prologix GPIB
│   │   ├── instrument_ui.py       # FunGenInstrument + FunGenConfUi
│   │   └── conf_ui.ui             # Qt Designer UI file
│   │
│   ├── Lockin/                    # Lock-in Amplifier component
│   │   ├── __init__.py            # AnfatecLockin component class
│   │   ├── anfatec_driver.py      # Anfatec AMU 2.4 driver + VirtualLockin
│   │   ├── LI5655.py              # NF LI5655/LI5660 driver
│   │   ├── instrument_ui.py       # LockinInstrument + LockinUI + LockinGraphs
│   │   ├── conf.ui                # Configuration UI
│   │   ├── graphs.ui              # Real-time graphs dialog
│   │   └── demo.txt               # Demo data file
│   │
│   ├── Platina/                   # Translation Stage (motor) component
│   │   ├── __init__.py            # PlatinaComponent class
│   │   ├── motor.py               # Motor driver using libximc
│   │   ├── instrument_ui.py       # PlatinaInstrument + PlatinaUI
│   │   ├── motor_test.py          # Motor testing utilities
│   │   ├── conf.ui                # Configuration UI
│   │   └── *.cfg                  # Motor configuration files
│   │
│   ├── CameraPlatina/             # Camera + Stage integration
│   │   ├── __init__.py            # CameraPlatinaComponent class
│   │   ├── camera.py              # CameraBackend, VirtualCamera, LucamCam
│   │   ├── instrument_ui.py       # CameraPlatinaInstrument + UIs
│   │   ├── calibration.py         # CalibrationUI for pixel-to-distance
│   │   ├── custom_image.py        # ImageWidget for clickable images
│   │   ├── conf.ui                # Configuration UI
│   │   ├── calibration.ui         # Calibration dialog UI
│   │   └── camera_calibration.npy # Stored calibration data
│   │
│   ├── Oven/                      # Temperature Control component
│   │   ├── __init__.py            # LinkamOven component class
│   │   ├── TMS94.py               # Linkam TMS94 driver + VirtualOven
│   │   ├── instrument_ui.py       # OvenInstrument + OvenUI
│   │   └── conf.ui                # Configuration UI
│   │
│   ├── USBDAQ/                    # DAQ board component (focus control)
│   │   ├── __init__.py            # USB2527DAC component class
│   │   ├── USB2527.py             # MCC USB-2527 driver + VirtualDAC
│   │   ├── instrument_ui.py       # DACInstrument + DACUI + DACGraphs
│   │   ├── conf.ui                # Configuration UI
│   │   └── graphs.ui              # Real-time graphs dialog
│   │
│   ├── LinePlotter/               # Line graph visualization
│   ├── BarPlotter/                # Bar/histogram visualization
│   └── ScatterPlotter/            # Scatter plot visualization
│
├── Documentation/                 # Screenshots for documentation
│
├── preprod/                       # Pre-production/testing code
│
└── demo/                          # Demo configuration files
    └── run_conf.json              # Sample experiment configuration
```

---

## 4. Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11.4+ | Primary programming language |
| **PyQt5** | 5.15+ | GUI framework |
| **Lantz** | git | Hardware driver abstraction framework |
| **SER** | git | Scientific Experiment Runner framework |
| **pyqtgraph** | 0.13.7 | Real-time plotting |
| **OpenCV** | 4.10+ | Camera/image processing |
| **NumPy** | 1.26+ | Numerical computations |
| **Pandas** | 2.2+ | Data manipulation |
| **PyVISA** | 1.14+ | VISA instrument communication |

### External Hardware Libraries

| Library | Purpose | Installation |
|---------|---------|--------------|
| **libximc** | Standa motor controller interface | pip (included in requirements) |
| **lucam** | Lumenera camera SDK | pip (included in requirements) |
| **mcculw** | Measurement Computing DAQ | pip (included in requirements) |
| **Lockin.dll** | Anfatec lock-in amplifier | Manual installation to `components/Lockin/` |

### Key Dependencies from requirements.txt

```
opencv-python          # Camera and image processing
keyboard               # Keyboard input for motor control
libximc                # Standa motor controller
lucam                  # Lumenera camera SDK
pillow                 # Image processing
matplotlib             # Auxiliary plotting
mcculw                 # MCC DAQ library
pyqtgraph              # Real-time plotting
SER @ git+https://github.com/FranciscoGauna/SER.git
lantz.drivers @ git+https://github.com/lantzproject/lantz-drivers.git
PyVISA-py              # VISA instrument communication
```

---

## 5. Core Frameworks

### SER Framework

The SER (Scientific Experiment Runner) framework provides the experiment sequencing infrastructure. It manages:

- Configuration UI generation and layout
- Experiment execution loop
- Data collection and aggregation
- Results display and export

**Key SER Interfaces:**

```python
from SER.interfaces import (
    Component,                 # Base class for hardware components
    ComponentInitialization,   # Wrapper with position/name info
    ConfigurableInstrument,    # Devices that configure before measurement
    ObservableInstrument,      # Devices that observe/measure data
    ConfigurationUI,           # UI widgets for configuration
    ProcessDataUI,             # Real-time data visualization
    FinalDataUI,               # Final data visualization
)
from SER import get_main_widget  # Creates the main experiment UI
```

**Interface Details:**

1. **ConfigurableInstrument**: For devices that need configuration before each measurement point
   ```python
   class MyInstrument(ConfigurableInstrument):
       def configure(self, *args) -> Dict[str, Any]:
           """Execute configuration and return results"""
           pass
       
       def get_points(self) -> Generator:
           """Generate configuration points"""
           pass
       
       def point_amount(self) -> int:
           """Return total number of points"""
           pass
   ```

2. **ObservableInstrument**: For devices that measure/observe data
   ```python
   class MyObserver(ObservableInstrument):
       def observe(self) -> Dict[str, Any]:
           """Take a measurement and return results"""
           pass
   ```

3. **ConfigurationUI**: For device configuration widgets
   ```python
   class MyConfigUI(ConfigurationUI):
       gui = "path/to/ui_file.ui"
       
       def __init__(self, backend):
           super().__init__(backend=backend)
   ```

### Lantz Framework

Lantz provides hardware driver abstraction with Qt integration. Key features:

- **Feats**: Property-like accessors for hardware parameters
- **Qt Wrapping**: Thread-safe GUI integration
- **Units**: Physical unit handling

**Key Lantz Components:**

```python
from lantz import Driver, Feat
from lantz.qt import wrap_driver_cls
from lantz.qt.connect import connect_feat
```

**Driver Example:**

```python
from lantz import Driver, Feat

class MyHardwareDriver(Driver):
    @Feat(units="Hz", limits=(0, 100000))
    def frequency(self):
        """Read current frequency from hardware"""
        return self._query_frequency()
    
    @frequency.setter
    def frequency(self, value):
        """Set frequency on hardware"""
        self._send_frequency_command(value)
```

---

## 6. Component System

### Component Structure

Every hardware component follows this pattern:

```python
from SER.interfaces import Component
from lantz.qt import wrap_driver_cls

class MyComponent(Component):
    """Component wrapping a hardware device"""
    
    @classmethod
    def virtual(cls):
        """Factory method for virtual/test mode"""
        driver = wrap_driver_cls(VirtualDriver)()
        self = cls()
        self.instrument = MyInstrument(driver)
        self.conf_ui = MyConfigUI(self.instrument)
        return self
    
    @classmethod
    def real(cls, *connection_args):
        """Factory method for real hardware"""
        driver = wrap_driver_cls(RealDriver)(*connection_args)
        self = cls()
        self.instrument = MyInstrument(driver)
        self.conf_ui = MyConfigUI(self.instrument)
        return self
    
    def close_component(self):
        """Cleanup when component is closed"""
        if hasattr(self, 'driver'):
            self.driver.finalize()
```

### ComponentInitialization

The `ComponentInitialization` class wraps components with metadata for the SER framework:

```python
from SER.interfaces import ComponentInitialization

# Parameters: component, position_priority, row, column, name
fungen_init = ComponentInitialization(
    component=fungen_comp,    # The Component instance
    position_priority=0,      # Execution order priority
    row=0,                    # Grid row in configuration UI
    column=1,                 # Grid column in configuration UI
    name="Fungen 1"           # Display name (also used as data key prefix)
)
```

### Component Registration

Components are registered in `UI/main_window.py`:

```python
class MainWindow(QMainWindow):
    def load_options(self):
        # Define factory methods for each device option
        self.fungen_ops = {
            "Virtual": HPFunGen.virtual,
            "HP 33120A": lambda: HPFunGen.via_prologix_gpib(addr),
            "Rigol DG1022": HPFunGen.rigol
        }
        self.fungen_cb.addItems(self.fungen_ops.keys())
        
        # ... similar for other components
    
    def switch_window(self):
        # Create components based on user selection
        self.fungen_comp = self.fungen_ops[self.fungen_cb.currentText()]()
        fungen_init = ComponentInitialization(self.fungen_comp, 0, 0, 1, "Fungen 1")
        
        # Pass to SER framework
        ser_widget = get_main_widget(
            configurable=[fungen_init, platina_init, oven_init],
            observable=[lockin_init, dac_init],
            process_data_uis=[...],
            final_data_uis=[...],
        )
```

---

## 7. Hardware Components Reference

### 7.1 HP33120AFunGen (Function Generator)

**Location:** `components/HP33120AFunGen/`

**Supported Devices:**
- HP 33120A (via Prologix GPIB adapter)
- Rigol DG1022 (via USB)
- Virtual (for testing)

**Key Files:**
| File | Purpose |
|------|---------|
| `__init__.py` | `HPFunGen` component class with factory methods |
| `hp33120A_fungen.py` | HP 33120A driver + `VirtualFungen` |
| `RigolAdapter.py` | Adapter for Rigol DG1022 to match HP interface |
| `dll_wrapper.py` | FTDI USB wrapper for Prologix GPIB adapter |
| `instrument_ui.py` | `FunGenInstrument` + `FunGenConfUi` |

**Configurable Parameters:**
- Waveform type (SIN, SQU, TRI, RAMP, NOIS, DC, USER)
- Frequency range (linear or logarithmic sweep)
- Amplitude and DC offset

### 7.2 Lockin (Lock-in Amplifier)

**Location:** `components/Lockin/`

**Supported Devices:**
- Anfatec AMU 2.4 (via DLL)
- NF LI5655/LI5660 (via VISA/USB)
- Virtual/Demo (for testing)

**Key Files:**
| File | Purpose |
|------|---------|
| `__init__.py` | `AnfatecLockin` component class |
| `anfatec_driver.py` | Anfatec driver + `VirtualLockin` + `DemoLockin` |
| `LI5655.py` | NF LI5655/LI5660 driver |
| `instrument_ui.py` | `LockinInstrument` + `LockinUI` + `LockinGraphs` |

**Observable Outputs:**
- Amplitude (V)
- Phase (degrees)
- Real-time monitoring graphs

### 7.3 Platina (Translation Stage)

**Location:** `components/Platina/`

**Supported Devices:**
- Any XIMC-compatible motor from Standa
- Virtual (emulated motor)

**Key Files:**
| File | Purpose |
|------|---------|
| `__init__.py` | `PlatinaComponent` class |
| `motor.py` | `Motor` class using libximc, `get_available_motors()` |
| `instrument_ui.py` | `PlatinaInstrument` + `PlatinaUI` |
| `*.cfg` | Motor configuration files (XIMC format) |

**Features:**
- Synchronous and asynchronous movement
- Position feedback with encoder support
- Backlash compensation
- Speed/acceleration control
- Keyboard-controlled jog movement

### 7.4 CameraPlatina (Camera + Stage Integration)

**Location:** `components/CameraPlatina/`

**Supported Cameras:**
- Lumenera Infinity 1 (via lucam SDK)
- Any OpenCV-compatible webcam
- Virtual (for testing)

**Key Files:**
| File | Purpose |
|------|---------|
| `__init__.py` | `CameraPlatinaComponent` class |
| `camera.py` | `CameraBackend`, `VirtualCamera`, `LucamCam` |
| `instrument_ui.py` | `CameraPlatinaInstrument` + UI classes |
| `calibration.py` | `CalibrationUI` for pixel-to-distance calibration |
| `custom_image.py` | `ImageWidget` for clickable image display |

**Features:**
- Live camera preview
- Click-to-define scan path
- Pixel-to-motor calibration
- Square (grid) or Line scan modes

### 7.5 Oven (Temperature Control)

**Location:** `components/Oven/`

**Supported Devices:**
- Linkam TMS 94 (via serial)
- Virtual (for testing)

**Key Files:**
| File | Purpose |
|------|---------|
| `__init__.py` | `LinkamOven` component class |
| `TMS94.py` | `LinkamTMS94` driver + `VirtualOven` |
| `instrument_ui.py` | `OvenInstrument` + `OvenUI` |

**Configurable Parameters:**
- Temperature range
- Heating rate

### 7.6 USBDAQ (DAQ Board / Focus Control)

**Location:** `components/USBDAQ/`

**Supported Devices:**
- MCC USB-2527 (via mcculw)
- Virtual (for testing)

**Key Files:**
| File | Purpose |
|------|---------|
| `__init__.py` | `USB2527DAC` component class |
| `USB2527.py` | `USB2527Driver` + `VirtualDAC` |
| `instrument_ui.py` | `DACInstrument` + `DACUI` + `DACGraphs` + `DACStatus` |

**Features:**
- Analog input/output
- Digital I/O for laser control
- Real-time focus monitoring
- ABCD photodiode sum and focus error signals

### 7.7 Visualization Components

**LinePlotter** (`components/LinePlotter/`):
- Real-time line/scatter plotting
- Implements `ProcessDataUI` interface

**BarPlotter** (`components/BarPlotter/`):
- Bar graphs and histograms
- Implements `ProcessDataUI` and `FinalDataUI` interfaces

---

## 8. Data Flow and Application Lifecycle

### Application Startup

```
main.py
    │
    ├── Create QApplication
    ├── Initialize logging
    │
    └── MainWindow.__init__()
            │
            ├── Load UI from main_window.ui
            ├── load_options()  # Populate device ComboBoxes
            └── show()
```

### Device Initialization Flow

```
User clicks "Launch" button
    │
    └── MainWindow.switch_window()
            │
            ├── For each device type:
            │   │
            │   ├── Get factory method from ops dict
            │   │   fungen_ops[combobox.currentText()]()
            │   │
            │   ├── Factory creates driver
            │   │   driver = wrap_driver_cls(DriverClass)()
            │   │
            │   ├── Factory creates component
            │   │   component.instrument = Instrument(driver)
            │   │   component.conf_ui = ConfigUI(instrument)
            │   │
            │   └── Wrap in ComponentInitialization
            │       ComponentInitialization(component, priority, row, col, name)
            │
            ├── Create visualization components
            │   LinePlotter, BarPlotter, etc.
            │
            └── Call SER.get_main_widget()
                    │
                    ├── configurable_components
                    ├── observable_components
                    ├── process_data_uis
                    └── final_data_uis
```

### Experiment Execution Flow

```
User clicks "Run" in SER widget
    │
    └── SER Framework Execution Loop
            │
            ├── For each configuration point:
            │   │
            │   ├── Call configurable.configure(*point)
            │   │   └── Returns Dict with configuration data
            │   │
            │   ├── Wait for stabilization (if configured)
            │   │
            │   ├── Call observable.observe()
            │   │   └── Returns Dict with measurement data
            │   │
            │   ├── Aggregate data from all components
            │   │
            │   ├── Call process_ui.add_data(data)
            │   │   └── Update real-time visualizations
            │   │
            │   └── Store data row
            │
            └── On completion:
                    │
                    ├── Call final_ui.set_data(all_data)
                    └── Enable data export
```

### Data Output Format

Experiment data is collected as dictionaries and exported as CSV:

```csv
time,Platina_motor_x_position,Platina_motor_y_position,Fungen 1_frequency,Lockin_amplitude,Lockin_phase,...
0.0,0.0,0.0,100.0,0.00123,45.2,...
0.5,1.0,0.0,200.0,0.00098,42.1,...
```

Column names are generated from: `{component_name}_{variable_name}`

---

## 9. Threading Model

The application uses multiple threads for responsive UI:

### Thread Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Main Thread                               │
│                    PyQt5 Event Loop                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  UI Updates, User Input, Signal/Slot Connections            ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
           │
           ├──────────────────────────────────────────────────────┐
           │                                                      │
┌──────────▼──────────┐  ┌───────────────────┐  ┌────────────────▼────────┐
│  Motor Status       │  │  Camera Thread    │  │  DAC Status Thread      │
│  Thread             │  │                   │  │                         │
│  (Motor.MotorStatus)│  │  (CameraPlatinaUI)│  │  (DACStatus)            │
│                     │  │                   │  │                         │
│  Polls motor        │  │  Captures frames  │  │  Reads analog inputs    │
│  position @ 100Hz   │  │  continuously     │  │  continuously           │
└─────────────────────┘  └───────────────────┘  └─────────────────────────┘
           │
           └──────────────────────────────────────────────────────┐
                                                                  │
┌─────────────────────────────────────────────────────────────────▼───────┐
│                       Lockin Graph Thread                                │
│                       (LockinGraphs)                                     │
│                                                                          │
│  Continuous lock-in monitoring for real-time amplitude/phase display   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Thread-Safe Status Updates Pattern

```python
from threading import Thread
from time import sleep

class StatusMonitor:
    def __init__(self):
        self.running = True
        self.thread = Thread(target=self._update_loop, daemon=True)
        self.thread.start()
    
    def _update_loop(self):
        while self.running:
            self._read_and_update_status()
            sleep(0.01)  # 100 Hz polling
    
    def stop(self):
        self.running = False
        self.thread.join(timeout=1.0)
```

### Qt Signal/Slot for Thread-Safe UI Updates

When updating UI from background threads, use Qt signals:

```python
from PyQt5.QtCore import pyqtSignal, QObject

class DataEmitter(QObject):
    data_ready = pyqtSignal(dict)

class BackgroundWorker:
    def __init__(self, ui_widget):
        self.emitter = DataEmitter()
        self.emitter.data_ready.connect(ui_widget.update_display)
    
    def _worker_thread(self):
        while self.running:
            data = self._read_hardware()
            self.emitter.data_ready.emit(data)  # Thread-safe UI update
```

---

## 10. Adding New Components

### Step-by-Step Guide

#### Step 1: Create Component Directory

```bash
mkdir components/NewDevice
touch components/NewDevice/__init__.py
touch components/NewDevice/driver.py
touch components/NewDevice/instrument_ui.py
```

#### Step 2: Create the Driver

`components/NewDevice/driver.py`:

```python
from lantz import Driver, Feat, Action

class NewDeviceDriver(Driver):
    """Driver for real hardware"""
    
    def __init__(self, *connection_args):
        super().__init__()
        # Initialize connection
    
    def initialize(self):
        """Called when driver is opened"""
        pass
    
    def finalize(self):
        """Called when driver is closed"""
        pass
    
    @Feat(units="Hz", limits=(0, 100000))
    def frequency(self):
        """Get current frequency"""
        return self._query("FREQ?")
    
    @frequency.setter
    def frequency(self, value):
        """Set frequency"""
        self._send(f"FREQ {value}")
    
    @Action()
    def reset(self):
        """Reset device to defaults"""
        self._send("*RST")


class VirtualNewDevice(Driver):
    """Virtual driver for testing without hardware"""
    
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

#### Step 3: Create Instrument and Configuration UI

`components/NewDevice/instrument_ui.py`:

```python
from typing import Dict, Any, Generator
from SER.interfaces import ConfigurableInstrument, ConfigurationUI
from lantz.qt.connect import connect_feat
import numpy as np

class NewDeviceInstrument(ConfigurableInstrument):
    """Instrument logic wrapping the driver"""
    
    def __init__(self, driver):
        self.driver = driver
        self._start_freq = 100
        self._end_freq = 10000
        self._steps = 10
        self._log_scale = True
    
    def configure(self, frequency) -> Dict[str, Any]:
        """Configure device for measurement point"""
        self.driver.frequency = frequency
        return {"frequency": frequency}
    
    def get_points(self) -> Generator:
        """Generate configuration points"""
        if self._log_scale:
            freqs = np.logspace(
                np.log10(self._start_freq),
                np.log10(self._end_freq),
                self._steps
            )
        else:
            freqs = np.linspace(self._start_freq, self._end_freq, self._steps)
        
        for freq in freqs:
            yield (freq,)
    
    def point_amount(self) -> int:
        """Return total number of points"""
        return self._steps
    
    def get_config(self) -> Dict[str, Any]:
        """Export current configuration"""
        return {
            "start_freq": self._start_freq,
            "end_freq": self._end_freq,
            "steps": self._steps,
            "log_scale": self._log_scale,
        }
    
    def set_config(self, config: Dict[str, Any]):
        """Import configuration"""
        self._start_freq = config.get("start_freq", self._start_freq)
        self._end_freq = config.get("end_freq", self._end_freq)
        self._steps = config.get("steps", self._steps)
        self._log_scale = config.get("log_scale", self._log_scale)


class NewDeviceUI(ConfigurationUI):
    """Configuration UI widget"""
    
    gui = "conf.ui"  # Path to Qt Designer .ui file
    
    def __init__(self, backend: NewDeviceInstrument):
        super().__init__(backend=backend)
        
        # Connect UI widgets to instrument properties
        # Assuming conf.ui has spinboxes: start_freq_spin, end_freq_spin, steps_spin
        # and a checkbox: log_scale_check
        
        self.widget.start_freq_spin.valueChanged.connect(
            lambda v: setattr(self.backend, '_start_freq', v)
        )
        self.widget.end_freq_spin.valueChanged.connect(
            lambda v: setattr(self.backend, '_end_freq', v)
        )
        self.widget.steps_spin.valueChanged.connect(
            lambda v: setattr(self.backend, '_steps', v)
        )
        self.widget.log_scale_check.toggled.connect(
            lambda v: setattr(self.backend, '_log_scale', v)
        )
        
        # If connecting to Lantz Feats on the driver:
        # connect_feat(self.widget.freq_spin, self.backend.driver, "frequency")
```

#### Step 4: Create the Component Class

`components/NewDevice/__init__.py`:

```python
from SER.interfaces import Component
from lantz.qt import wrap_driver_cls
from .driver import NewDeviceDriver, VirtualNewDevice
from .instrument_ui import NewDeviceInstrument, NewDeviceUI

class NewDeviceComponent(Component):
    """Component for NewDevice hardware"""
    
    @classmethod
    def virtual(cls):
        """Create component with virtual driver (for testing)"""
        driver = wrap_driver_cls(VirtualNewDevice)()
        self = cls()
        self.instrument = NewDeviceInstrument(driver)
        self.conf_ui = NewDeviceUI(self.instrument)
        return self
    
    @classmethod
    def real(cls, port: str):
        """Create component with real hardware"""
        driver = wrap_driver_cls(NewDeviceDriver)(port)
        driver.initialize()
        self = cls()
        self.driver = driver  # Store for cleanup
        self.instrument = NewDeviceInstrument(driver)
        self.conf_ui = NewDeviceUI(self.instrument)
        return self
    
    def close_component(self):
        """Cleanup when component is closed"""
        if hasattr(self, 'driver'):
            self.driver.finalize()
```

#### Step 5: Create the UI File

Use Qt Designer to create `components/NewDevice/conf.ui` with appropriate widgets.

Alternatively, create programmatically:

```python
# In instrument_ui.py, override gui with None and build UI in __init__
class NewDeviceUI(ConfigurationUI):
    gui = None
    
    def __init__(self, backend):
        super().__init__(backend=backend)
        
        from PyQt5.QtWidgets import QVBoxLayout, QSpinBox, QLabel, QCheckBox
        
        layout = QVBoxLayout()
        
        self.start_freq_spin = QSpinBox()
        self.start_freq_spin.setRange(1, 100000)
        layout.addWidget(QLabel("Start Frequency (Hz)"))
        layout.addWidget(self.start_freq_spin)
        
        # ... add more widgets
        
        self.widget.setLayout(layout)
```

#### Step 6: Register in MainWindow

Edit `UI/main_window.py`:

```python
from components.NewDevice import NewDeviceComponent

class MainWindow(QMainWindow):
    def load_options(self):
        # ... existing code ...
        
        self.newdevice_ops = {
            "Virtual": NewDeviceComponent.virtual,
            "Real": lambda: NewDeviceComponent.real("COM3"),
        }
        self.newdevice_cb.addItems(self.newdevice_ops.keys())
    
    def switch_window(self):
        # ... existing code ...
        
        self.newdevice_comp = self.newdevice_ops[self.newdevice_cb.currentText()]()
        newdevice_init = ComponentInitialization(
            self.newdevice_comp, 
            position_priority=0,  # Adjust as needed
            row=0, 
            column=2,  # Adjust grid position
            name="NewDevice"
        )
        
        # Add to configurable or observable list
        ser_widget = get_main_widget(
            configurable=[..., newdevice_init],
            # or observable=[..., newdevice_init],
            ...
        )
```

#### Step 7: Update main_window.ui

Add a ComboBox and Label for the new device in Qt Designer, or add programmatically.

---

## 11. Configuration System

### Runtime Configuration (devices.ini)

The `devices.ini` file stores connection parameters for hardware devices. It is auto-generated on first run with default values.

**Location:** Same directory as `main.py`

**Format:**
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

**How it works in code:**

```python
# UI/main_window.py
from configparser import ConfigParser

config = ConfigParser()

# Default values
config["HP33120AFungen"] = {"PROLOGIX ADDR": "10"}
config["Web Cam"] = {"Index": "0"}
# ...

# Load or create file
if path.exists("devices.ini"):
    config.read("devices.ini")
else:
    with open("devices.ini", "w") as f:
        config.write(f)

# Use in factory methods
lambda: HPFunGen.via_prologix_gpib(int(config["HP33120AFungen"]["PROLOGIX ADDR"]))
```

### Adding New Configuration Options

1. Add default value in `MainWindow`:
   ```python
   config["NewDevice"] = {"Port": "COM3", "Baudrate": "9600"}
   ```

2. Use in factory method:
   ```python
   self.newdevice_ops = {
       "Real": lambda: NewDeviceComponent.real(
           config["NewDevice"]["Port"],
           int(config["NewDevice"]["Baudrate"])
       ),
   }
   ```

### Experiment Configuration (JSON)

Experiment parameters can be saved/loaded as JSON:

```python
# Save configuration
config_dict = {}
for component in components:
    config_dict[component.name] = component.instrument.get_config()

with open("experiment_config.json", "w") as f:
    json.dump(config_dict, f, indent=2)

# Load configuration
with open("experiment_config.json", "r") as f:
    config_dict = json.load(f)

for component in components:
    if component.name in config_dict:
        component.instrument.set_config(config_dict[component.name])
```

### Motor Configuration Files (.cfg)

Motor configuration files are in XIMC format and located in `components/Platina/`:

| File | Motor |
|------|-------|
| `8MT173-10.cfg` | Standa 8MT173-10 |
| `8MT173-10-Encoder.cfg` | Same with encoder |
| `8MTF-75LS05-Encoder-x.cfg` | X-axis with encoder |
| `8MTF-75LS05-Encoder-y.cfg` | Y-axis with encoder |
| `flash_eje_x.cfg` | Flash stage X-axis |
| `flash_eje_y.cfg` | Flash stage Y-axis |

---

## 12. Testing and Development

### Running in Virtual Mode

All components support "Virtual" mode for testing without hardware:

```bash
python main.py
# Select "Virtual" for all device dropdowns
# Click "Lanzar" (Launch)
```

### Demo Configuration

Load demo configuration from `demo/run_conf.json`:

```python
# In the SER widget, use the load configuration feature
# to import demo/run_conf.json
```

### Component Testing

Individual component tests can be run from `preprod/` or component directories:

```bash
# Test motor
python -m components.Platina.motor_test

# Test lock-in
python preprod/lockin.py

# Test camera
python preprod/camera.py
```

### Debug Entry Point

Use `debug_main.py` for development testing:

```bash
python debug_main.py
```

### Creating Mock Data

For `DemoLockin`, data is loaded from `components/Lockin/demo.txt`:

```
# demo.txt format (tab-separated)
amplitude   phase
0.001       45.2
0.002       42.1
...
```

### Logging

The application uses Lantz's logging system:

```python
from lantz.core.log import log_to_screen
from logging import DEBUG, INFO, WARNING, ERROR

# In main.py
log_to_screen(ERROR)  # Only show errors

# For development, use DEBUG
log_to_screen(DEBUG)
```

---

## 13. Common Patterns and Best Practices

### Lantz Driver Pattern

```python
from lantz import Driver, Feat, Action

class MyDriver(Driver):
    @Feat(units="Hz", limits=(0, 100000))
    def frequency(self):
        return self._freq
    
    @frequency.setter
    def frequency(self, value):
        self._freq = value
        self._send_to_hardware(value)
    
    @Action()
    def reset(self):
        self._send("*RST")
```

### Qt UI Loading Pattern

```python
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from os import path

class MyUI(QWidget):
    def __init__(self):
        super().__init__()
        ui_path = path.join(
            path.dirname(path.realpath(__file__)), 
            "my_ui.ui"
        )
        uic.loadUi(ui_path, self)
```

### Feature Connection Pattern

```python
from lantz.qt.connect import connect_feat

# Connects a QSpinBox to a Lantz Feat
connect_feat(self.widget.spinbox, self.driver, "frequency")
# Now changes to spinbox automatically update driver.frequency
# and changes to driver.frequency update the spinbox
```

### Thread-Safe Status Monitoring

```python
from threading import Thread
from time import sleep

class StatusMonitor:
    def __init__(self):
        self.running = True
        self.thread = Thread(target=self._update_loop, daemon=True)
        self.thread.start()
    
    def _update_loop(self):
        while self.running:
            self._read_status()
            sleep(0.01)
    
    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
```

### Signal Emission for Real-Time Data

```python
from PyQt5.QtCore import pyqtSignal

class DataSource(QObject):
    new_data = pyqtSignal(float, float)  # amplitude, phase
    
    def read_data(self):
        amp, phase = self.driver.read()
        self.new_data.emit(amp, phase)

# In UI class
self.data_source.new_data.connect(self.update_plot)
```

### Error Handling in Drivers

```python
class MyDriver(Driver):
    @Feat
    def value(self):
        try:
            response = self._query("VAL?")
            return float(response)
        except (ValueError, TimeoutError) as e:
            self.log_error(f"Failed to read value: {e}")
            raise
```

---

## 14. Troubleshooting Development Issues

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'SER'`

**Solution:**
```bash
pip install git+https://github.com/FranciscoGauna/SER.git
```

### Driver Connection Issues

**Problem:** Driver fails to connect to hardware

**Debug Steps:**
1. Test hardware with manufacturer's software first
2. Check connection parameters (port, address, etc.)
3. Verify driver installation (check `pip list`)
4. Try virtual mode to isolate hardware issues
5. Add debug logging:
   ```python
   from lantz.core.log import log_to_screen
   from logging import DEBUG
   log_to_screen(DEBUG)
   ```

### UI Not Updating from Background Thread

**Problem:** UI freezes or doesn't update when hardware changes

**Solution:** Use Qt signals for thread-safe updates:
```python
# Wrong (crashes or freezes)
def background_thread(self):
    while True:
        data = self.read_hardware()
        self.label.setText(str(data))  # DON'T DO THIS

# Correct
class Emitter(QObject):
    update = pyqtSignal(str)

def background_thread(self):
    while True:
        data = self.read_hardware()
        self.emitter.update.emit(str(data))

# Connect in __init__
self.emitter.update.connect(self.label.setText)
```

### Motor Not Moving

**Debug Steps:**
1. Check XIMC software installation
2. Verify motor is detected: `get_available_motors()`
3. Check configuration file matches motor model
4. Test with motor_test.py

### Camera Shows Black Image

**Debug Steps:**
1. Check camera index in `devices.ini`
2. Test with OpenCV directly:
   ```python
   import cv2
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   print(f"Success: {ret}, Shape: {frame.shape if ret else 'N/A'}")
   ```
3. Verify no other application is using the camera

### PyQt UI File Not Loading

**Problem:** `uic.loadUi()` fails

**Solution:**
- Verify .ui file path is correct
- Use absolute path:
  ```python
  ui_path = path.join(path.dirname(path.realpath(__file__)), "conf.ui")
  ```
- Check .ui file isn't corrupted (open in Qt Designer)

---

## 15. External Resources

### Documentation

| Resource | URL |
|----------|-----|
| SER Framework | https://github.com/FranciscoGauna/SER |
| Lantz Documentation | https://lantz.readthedocs.io/ |
| XIMC Motor Documentation | https://files.xisupport.com/Software.en.html |
| PyQt5 Documentation | https://www.riverbankcomputing.com/static/Docs/PyQt5/ |
| pyqtgraph Documentation | https://pyqtgraph.readthedocs.io/ |

### Hardware Manufacturer Links

| Device | Manufacturer | Link |
|--------|--------------|------|
| Lock-in AMU 2.4 | Anfatec | https://www.anfatec.de/ |
| Translation Stages | Standa | https://www.standa.lt/ |
| Cameras | Lumenera | https://www.lumenera.com/ |
| DAQ Boards | Digilent/MCC | https://www.mccdaq.com/ |
| Linkam Stages | Linkam | https://www.linkam.co.uk/ |

### Development Tools

| Tool | Purpose |
|------|---------|
| Qt Designer | UI layout design |
| NI MAX | VISA device discovery |
| Anaconda | Python environment management |

---

## Appendix A: Quick Reference

### Creating a New Component Checklist

- [ ] Create directory `components/NewDevice/`
- [ ] Create `driver.py` with real and virtual drivers
- [ ] Create `instrument_ui.py` with instrument and UI classes
- [ ] Create `__init__.py` with component class and factory methods
- [ ] Create `conf.ui` using Qt Designer (optional)
- [ ] Add to `UI/main_window.py`:
  - [ ] Import component
  - [ ] Add to ops dictionary in `load_options()`
  - [ ] Add ComboBox items
  - [ ] Create component in `switch_window()`
  - [ ] Add to SER `get_main_widget()` call
- [ ] Update `main_window.ui` with new ComboBox (optional)
- [ ] Add configuration to `devices.ini` defaults
- [ ] Test in virtual mode
- [ ] Test with real hardware

### SER Interface Quick Reference

```python
# ConfigurableInstrument
configure(*args) -> Dict[str, Any]
get_points() -> Generator
point_amount() -> int

# ObservableInstrument
observe() -> Dict[str, Any]

# ConfigurationUI
gui: str  # Path to .ui file
backend: Instrument

# ProcessDataUI
add_data(data: Dict)

# FinalDataUI
set_data(data: List[Dict])

# ComponentInitialization
ComponentInitialization(component, priority, row, col, name)
```

### Lantz Quick Reference

```python
from lantz import Driver, Feat, Action
from lantz.qt import wrap_driver_cls
from lantz.qt.connect import connect_feat

# Wrap driver for Qt thread safety
WrappedDriver = wrap_driver_cls(MyDriver)
driver = WrappedDriver()

# Connect UI widget to Feat
connect_feat(widget, driver, "feat_name")
```

---

*This developer manual was created for the Microscopy-Program developed by Facundo Zaldivar Escola at the Laboratorio de Haces Dirigidos, Facultad de Ingenieria, Universidad de Buenos Aires.*
