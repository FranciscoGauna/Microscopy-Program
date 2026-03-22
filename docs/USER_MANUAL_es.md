# Manual de Usuario del Microscopy-Program

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Guía de Inicio Rápido](#guía-de-inicio-rápido)
5. [Selección de Dispositivos](#selección-de-dispositivos)
6. [Configuración del Experimento](#configuración-del-experimento)
7. [Ejecución de un Experimento](#ejecución-de-un-experimento)
8. [Exportación de Datos](#exportación-de-datos)
9. [Referencia de Configuración](#referencia-de-configuración)
10. [Resolución de Problemas](#resolución-de-problemas)
11. [Apéndice](#apéndice)

---

## Introducción

El Microscopy-Program es un software de control para un microscopio fototérmico desarrollado en el Laboratorio de Haces Dirigidos, Facultad de Ingeniería, Universidad de Buenos Aires.

### Qué Hace Este Software

Este software automatiza y coordina múltiples instrumentos de laboratorio para realizar experimentos de microscopía fototérmica:

- **Escaneo de Muestras**: Controla platinas de traslación motorizadas (ejes X, Y, Z) para escanear muestras
- **Generación de Señales**: Controla generadores de funciones para barridos de frecuencia
- **Medición de Señales**: Lee datos del amplificador lock-in para mediciones de precisión
- **Captura de Imágenes**: Captura y muestra imágenes de cámara para posicionamiento de muestras
- **Control de Temperatura**: Gestiona calentamiento con hornos de temperatura controlada
- **Control de Foco**: Monitorea y ajusta el foco usando retroalimentación láser

### Flujo de Trabajo General

```
┌───────────────────────────────┐
│  1. Selección de Dispositivos │  Seleccionar qué instrumentos usar
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│  2. Configuración             │  Establecer parámetros para cada dispositivo
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│  3. Ejecutar Experimento      │  Ejecutar con monitoreo en tiempo real
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│  4. Exportar Datos            │  Guardar resultados en formato CSV o MATLAB
└───────────────────────────────┘
```

---

## Requisitos del Sistema

### Sistema Operativo

- **Windows 10/11** (requerido para los drivers de hardware)

### Requisitos de Software

| Componente | Versión Mínima | Notas |
|------------|----------------|-------|
| Python | 3.11.4 | Se recomienda la distribución Anaconda |
| PyQt5 | 5.15+ | Framework de interfaz gráfica |

### Drivers de Hardware

Los siguientes drivers externos deben instalarse según el equipamiento disponible:

| Dispositivo | Driver | Enlace de Descarga |
|-------------|--------|-------------------|
| Lock-in AMU 2.4 | `AMU 2.4 Lockin.dll` | [Anfatec](https://www.anfatec.de/products/3_lockin/amu/24/pci-bus_lockin_amplifier_amu24.html) |
| Platina de Traslación | Paquete de Software XIMC | [Standa](https://files.xisupport.com/Software.en.html) |
| Cámara Lumenera | Software LgCam | [Lumenera](https://www.lumenera.com/support/industrial-usb-ethernet/drivers-downloads.html) |
| MCC DAQ | MCCDAQ UL para Windows | [Digilent](https://cloud.digilent.com/myproducts/ULxforWindows) |

---

## Instalación

### Paso 1: Instalar Python

1. Descargar Anaconda desde https://www.anaconda.com/download
2. Ejecutar el instalador y seguir las instrucciones
3. Verificar la instalación abriendo Anaconda Prompt y escribiendo:
   ```
   python --version
   ```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
conda create -n microscopy python=3.11
conda activate microscopy
```

### Paso 3: Instalar Dependencias de Python

Navegar al directorio del Microscopy-Program y ejecutar:

```bash
pip install -r requirements.txt
```

Para las versiones exactas probadas, usar:

```bash
pip install -r frozenreqs.txt
```

### Paso 4: Instalar Drivers de Hardware

Instalar los drivers apropiados para el equipamiento (ver tabla de Requisitos del Sistema arriba).

### Paso 5: Verificar la Instalación

Ejecutar el programa para verificar que todo esté instalado correctamente:

```bash
python main.py
```

Debería aparecer la ventana de selección de dispositivos.

---

## Guía de Inicio Rápido

### Ejecutando su Primer Experimento (Modo Virtual)

Esta guía lo lleva a través de una ejecución de prueba usando dispositivos virtuales (simulados).

1. **Iniciar el Programa**
   ```bash
   python main.py
   ```

2. **Seleccionar Dispositivos Virtuales**
   - Configurar todos los menús desplegables de dispositivos en opciones "Virtual"
   - Hacer clic en **Launch**

3. **Configurar un Escaneo Simple**
   - En la sección Motor X, configurar:
     - Inicial: 0
     - Final: 10
     - Pasos: 5
   - En la sección Generador de Funciones, configurar:
     - Frecuencia Inicial: 100
     - Frecuencia Final: 1000
     - Pasos: 10
     - Escala: Logarítmica

4. **Ejecutar el Experimento**
   - Hacer clic en el botón **Run**
   - Observar cómo se actualizan los gráficos en tiempo real

5. **Exportar Datos**
   - Después de completarse, ir a la pestaña Data
   - Hacer clic en **Save CSV** para exportar los resultados

---

## Selección de Dispositivos

Al iniciar el programa, verá la pantalla de selección de dispositivos:

![Selección de Dispositivos](Documentation/choose_devices.png)

### Dispositivos Disponibles

#### Generador de Funciones
| Opción | Descripción |
|--------|-------------|
| Virtual | Generador simulado para pruebas |
| HP 33120A | Generador de funciones HP vía adaptador GPIB/Prologix |
| Rigol DG1022 | Generador Rigol vía USB |

#### Amplificador Lock-in
| Opción | Descripción |
|--------|-------------|
| Virtual | Lock-in simulado con datos de demostración |
| Anfatec AMU 2.4 | Vía interfaz DLL |
| NF LI5655/LI5660 | Vía VISA/USB |

#### Platina de Traslación (Motores)
| Opción | Descripción |
|--------|-------------|
| Virtual | Motor simulado para pruebas |
| 8MT173-10 | Motor Standa 8MT173-10 con archivo de configuración |
| 8MTF-75LS05 | Motor Standa 8MTF-75LS05 con encoder |
| Flash Stage | Platina de posicionamiento rápido |
| Otros motores XIMC | Cualquier motor compatible con XIMC |

#### Cámara
| Opción | Descripción |
|--------|-------------|
| Virtual | Cámara simulada para pruebas |
| Lumenera Infinity 1 | Cámara profesional de microscopía |
| Web Cam | Cualquier webcam compatible con OpenCV |

#### Horno
| Opción | Descripción |
|--------|-------------|
| Virtual | Horno simulado para pruebas |
| Linkam TMS 94 | Platina con control de temperatura |

#### DAC (Conversor Digital-Analógico)
| Opción | Descripción |
|--------|-------------|
| Virtual | DAC simulado para pruebas |
| MCC USB-2527 | DAQ USB de Measurement Computing |

### Archivos de Configuración de Motores

Los archivos de configuración de motores (`.cfg`) definen parámetros específicos del motor:
- Tipo y dirección de retroalimentación
- Factor de conversión de cuentas a distancia
- Límites de velocidad y aceleración

Estos archivos se encuentran en `components/Platina/` y siguen el formato XIMC.

---

## Configuración del Experimento

Después de seleccionar dispositivos y hacer clic en **Launch**, verá la pantalla de configuración:

![Pantalla de Configuración](Documentation/configure_page.png)

### Sección de Cámara

La sección de cámara muestra una transmisión de video en vivo y permite definir trayectorias de escaneo.

**Características:**
- **Vista Previa en Vivo**: Imagen de cámara en tiempo real
- **Clic-para-Escanear**: Hacer clic en la imagen para definir posiciones del motor
- **Modo de Escaneo**: Elegir entre escaneo Cuadrado (grilla) o Línea

**Calibración:**

Para calibrar la conversión de píxeles a distancia:

1. Hacer clic en el botón **Calibrate**
2. Seguir las instrucciones en pantalla
3. Hacer clic en dos puntos de distancia conocida
4. Ingresar la distancia real

![Pantalla de Calibración](Documentation/configure_page_calibration.png)

### Sección de Motores

Cada motor (X, Y, Z) tiene su propio panel de configuración.

| Parámetro | Descripción |
|-----------|-------------|
| Posición Actual | Muestra la ubicación actual del motor |
| Inicial | Posición de inicio del escaneo |
| Final | Posición final del escaneo |
| Pasos | Número de puntos de medición |
| Velocidad | Velocidad de movimiento del motor |
| Aceleración | Tasa de aceleración del motor |
| Backlash | Compensación de holgura mecánica |

**Mover el Motor Manualmente:**
1. Ingresar una posición objetivo en el campo "Move to"
2. Hacer clic en el botón de movimiento
3. Usar **Stop** en caso de emergencia

**Establecer el Cero:**
- Hacer clic en el botón "Set Zero" para definir la posición actual como origen

**Ejemplos de Trayectoria de Escaneo:**

Para modo Cuadrado con Motor X (0→2, 3 pasos) y Motor Y (0→2, 3 pasos):
```
(0,0) → (1,0) → (2,0)
(0,1) → (1,1) → (2,1)
(0,2) → (1,2) → (2,2)
```

Para modo Línea con los mismos parámetros:
```
(0,0) → (1,1) → (2,2)
```

### Sección del Generador de Funciones

| Parámetro | Descripción |
|-----------|-------------|
| Frecuencia Inicial | Frecuencia de inicio en Hz |
| Frecuencia Final | Frecuencia final en Hz |
| Pasos | Número de puntos de frecuencia |
| Escala | Espaciado Lineal o Logarítmico |
| Amplitud | Amplitud de la señal en Volts |
| Offset | Offset DC en Volts |
| Forma de Onda | Forma de la señal (Seno, Cuadrada, Triángulo, etc.) |

**Ejemplo - Barrido Logarítmico:**
- Inicial: 10 Hz
- Final: 1000 Hz
- Pasos: 3
- Escala: Logarítmica
- Resultado: 10 Hz → 100 Hz → 1000 Hz

### Sección del Amplificador Lock-in

| Parámetro | Descripción |
|-----------|-------------|
| Constante de Tiempo | Tiempo de integración (afecta ruido vs. velocidad) |
| Sensibilidad | Configuración de ganancia de entrada |
| Pendiente | Caída del filtro (6, 12, 18 o 24 dB/oct) |
| Armónico | Qué armónico medir (1 = fundamental) |
| Referencia Externa | **Debe estar ACTIVADA para experimentos** |

**Gráficos en Tiempo Real:**

La sección del lock-in muestra gráficos en vivo que incluyen:
- Señal de reflectancia
- Señal de error

![Gráficos del Lock-in](Documentation/configure_page_lockin_graphs.png)

### Sección del Horno

| Parámetro | Descripción |
|-----------|-------------|
| Temperatura Inicial | Temperatura de inicio en °C |
| Temperatura Final | Temperatura final en °C |
| Pasos | Número de puntos de temperatura |
| Tasa | Tasa de calentamiento/enfriamiento en °C/min |

### Sección de DAC/Control de Foco

| Parámetro | Descripción |
|-----------|-------------|
| Láser Encendido/Apagado | Activar/desactivar láser de prueba |
| Potencia del Láser | Ajustar intensidad del láser |
| Control de Foco | Activar/desactivar autoenfoque (experimental) |

**Gráficos en Tiempo Real:**

![Gráficos de Control de Foco](Documentation/configure_page_dac_graphs.png)

- **Reflectancia**: Señal de reflectividad de la muestra
- **Suma ABCD**: Suma del fotodiodo para alineación
- **Error de Foco**: Señal de error para autoenfoque

### Acoplamiento de Dispositivos

El acoplamiento determina el orden en que varían los parámetros de los dispositivos durante el experimento.

**Regla:** Mayor número de acoplamiento = ciclo más rápido

**Ejemplo:**
- Acoplamiento del horno = 1, valores: 40°C, 50°C
- Acoplamiento del generador de funciones = 2, valores: 100 Hz, 1000 Hz

Secuencia de medición resultante:
```
(40°C, 100 Hz) → (40°C, 1000 Hz) → (50°C, 100 Hz) → (50°C, 1000 Hz)
```

---

## Ejecución de un Experimento

Después de configurar todos los parámetros, hacer clic en **Run** para iniciar el experimento.

![Experimento en Ejecución](Documentation/running_page.png)

### Monitoreo en Tiempo Real

Durante la ejecución, verá:
- **Gráfico de Fase**: Fase vs. log(frecuencia) en grados
- **Gráfico de Amplitud**: log(amplitud) vs. log(frecuencia) en Volts
- **Indicador de Progreso**: Punto actual / puntos totales

### Detener un Experimento

Hacer clic en el botón **Stop** para abortar el experimento en cualquier momento. Los datos recolectados hasta ese punto se preservarán.

---

## Exportación de Datos

Después de que el experimento se complete (o sea detenido), navegar a la pestaña Data.

![Tabla de Datos](Documentation/data_page.png)

### Visualización de Datos

La tabla de datos muestra todas las mediciones recolectadas con columnas para:
- Posiciones de motores
- Valores de frecuencia
- Amplitud y fase del lock-in
- Lecturas de temperatura
- Marcas de tiempo

### Guardar Documentación de Variables

1. Hacer clic en **Save Variables** (arriba a la izquierda)
2. Ingresar descripciones y unidades para cada variable
3. Estos metadatos se guardan junto con los datos

### Exportar Datos

| Formato | Botón | Descripción |
|---------|-------|-------------|
| CSV | Save CSV | Valores separados por comas, se abre en Excel |
| MATLAB | Save MATLAB | Archivo .mat para análisis en MATLAB |

---

## Referencia de Configuración

### devices.ini

Este archivo configura los parámetros de conexión para dispositivos de hardware. Se genera automáticamente en la primera ejecución.

```ini
[HP33120AFungen]
PROLOGIX ADDR = 10      ; Dirección GPIB para el generador de funciones HP

[Web Cam]
Index = 0               ; Índice de cámara de OpenCV

[Linkam TMS 94]
Port = 15               ; Número de puerto COM (15 = COM15)

[USB2527DAC]
Board Num = 0           ; Número de placa MCC
```

**Ubicación:** Mismo directorio que `main.py`

### Archivos de Configuración de Motores

Ubicados en `components/Platina/`, estos archivos `.cfg` definen parámetros del motor:

| Archivo | Modelo de Motor |
|---------|----------------|
| `8MT173-10.cfg` | Standa 8MT173-10 |
| `8MTF-75LS05-Encoder-X.cfg` | 8MTF-75LS05 eje X con encoder |
| `8MTF-75LS05-Encoder-Y.cfg` | 8MTF-75LS05 eje Y con encoder |
| `flash_eje_x.cfg` | Flash stage eje X |
| `flash_eje_y.cfg` | Flash stage eje Y |

---

## Resolución de Problemas

### Problemas de Conexión de Dispositivos

**Problema:** Dispositivo no encontrado

**Soluciones:**
1. Verificar que el dispositivo esté encendido y conectado
2. Comprobar las conexiones de cables USB/serial
3. Verificar la instalación del driver
4. Comprobar `devices.ini` para configuraciones correctas de puerto/dirección
5. Intentar desconectar y reconectar el dispositivo

**Problema:** Errores de "Permiso denegado"

**Soluciones:**
1. Ejecutar el programa como Administrador
2. Cerrar otros programas que puedan estar usando el dispositivo
3. Verificar que no haya otra instancia del Microscopy-Program ejecutándose

### Problemas con Motores

**Problema:** El motor no se mueve

**Soluciones:**
1. Verificar que el controlador del motor esté encendido
2. Verificar que el archivo de configuración correcto esté seleccionado
3. Comprobar la instalación del software XIMC
4. Intentar el botón "Home" para inicializar el motor

**Problema:** La posición del motor es incorrecta

**Soluciones:**
1. Re-establecer el cero del motor en una posición conocida
2. Verificar la conversión de cuentas a distancia en el archivo .cfg
3. Verificar la configuración de compensación de backlash

### Problemas con la Cámara

**Problema:** Sin imagen de cámara

**Soluciones:**
1. Verificar la conexión y alimentación de la cámara
2. Verificar que el driver correcto de la cámara esté instalado
3. Para webcam: intentar diferentes valores de índice en `devices.ini`
4. Verificar que ninguna otra aplicación esté usando la cámara

**Problema:** La imagen está oscura o sobreexpuesta

**Soluciones:**
1. Ajustar la configuración de exposición de la cámara (si está disponible)
2. Verificar la iluminación
3. Intentar una opción de cámara diferente

### Problemas con el Amplificador Lock-in

**Problema:** Sin señal / lecturas en cero

**Soluciones:**
1. Verificar que la referencia externa esté activada
2. Comprobar que el generador de funciones esté emitiendo señal
3. Verificar la configuración correcta de sensibilidad y constante de tiempo
4. Comprobar las conexiones de cables

**Problema:** Señal ruidosa

**Soluciones:**
1. Aumentar la constante de tiempo (más lento pero menos ruidoso)
2. Verificar si hay lazos de tierra
3. Verificar las conexiones de blindaje en los cables
4. Reducir interferencia electrónica cercana

### Problemas con la Exportación de Datos

**Problema:** No se pueden guardar los datos

**Soluciones:**
1. Verificar que tenga permisos de escritura en la carpeta de destino
2. Cerrar cualquier programa que pueda tener el archivo abierto
3. Intentar guardar en una ubicación diferente

### Problemas Generales

**Problema:** El programa se cierra al iniciar

**Soluciones:**
1. Verificar que todas las dependencias estén instaladas: `pip install -r requirements.txt`
2. Comprobar la versión de Python: `python --version` (debe ser 3.11+)
3. Intentar ejecutar en modo virtual (todos los dispositivos en Virtual)
4. Verificar los mensajes de error en la consola

**Problema:** El programa está lento o no responde

**Soluciones:**
1. Cerrar aplicaciones innecesarias en segundo plano
2. Reducir el número de puntos de medición
3. Verificar que haya suficiente espacio en disco
4. Reiniciar el programa

---

## Apéndice

### A. Formas de Onda Soportadas

| Forma de Onda | Descripción |
|---------------|-------------|
| Seno | Onda sinusoidal |
| Cuadrada | Onda cuadrada |
| Triángulo | Onda triangular |
| Rampa | Onda diente de sierra |
| Ruido | Ruido aleatorio |
| DC | Voltaje constante |

### B. Constantes de Tiempo del Lock-in

| Configuración | Tiempo de Respuesta | Caso de Uso |
|---------------|---------------------|-------------|
| 1 ms | Muy rápido | Mediciones de alta frecuencia |
| 10 ms | Rápido | Escaneos rápidos |
| 100 ms | Medio | Uso general |
| 1 s | Lento | Mediciones de bajo ruido |
| 10 s | Muy lento | Mediciones de precisión |

### C. Formatos de Archivo

**Formato CSV:**
```
time,motor_x,motor_y,frequency,amplitude,phase
0.0,0.0,0.0,100.0,0.00123,45.2
0.5,0.0,0.0,200.0,0.00098,42.1
...
```

**Formato MATLAB:**
- Archivo .mat estándar
- Las variables se almacenan como arreglos
- Los nombres de variables coinciden con los encabezados de columna

### D. Atajos de Teclado

| Tecla | Acción |
|-------|--------|
| Teclas de Flecha | Control manual del motor (cuando está habilitado) |
| Escape | Detener la operación actual |
| Ctrl+S | Guardar datos |

### E. Documentación Relacionada

- [Documentación del Framework SER](https://github.com/FranciscoGauna/SER) - Framework de secuenciación de experimentos
- [Documentación XIMC](https://files.xisupport.com/Software.en.html) - Documentación del controlador de motores
- [Drivers de Lantz](https://github.com/lantzproject/lantz-drivers) - Framework de drivers de hardware

### F. Contacto y Soporte

Para problemas y solicitudes de funcionalidades, contactar al equipo de desarrollo original en el Laboratorio de Haces Dirigidos, Facultad de Ingeniería, Universidad de Buenos Aires.

---

*Este manual fue escrito para el Microscopy-Program desarrollado por Facundo Zaldivar Escola.*
