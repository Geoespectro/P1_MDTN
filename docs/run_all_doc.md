# **Documentación del Script Lanzador `run_all.py`**

---

## **1. Descripción General del Script**

El script `run_all.py` tiene como objetivo ejecutar de manera concurrente las dos lógicas principales del proyecto: la descarga de los datos satelitales (`goes16Download.py`) y el procesamiento de estos datos (`main.py`). Para ello, utiliza `ThreadPoolExecutor` de la biblioteca `concurrent.futures`, permitiendo que ambas tareas se ejecuten en paralelo. Esto optimiza el flujo de trabajo, asegurando que el procesamiento de los datos pueda llevarse a cabo mientras la descarga continúa.

Este script permite que el sistema de descarga y procesamiento trabaje de manera coordinada, garantizando que ambos procesos se ejecuten de forma continua sin necesidad de intervención manual, lo cual es ideal para entornos donde la adquisición y análisis de datos se realicen de manera automatizada.

---

## **2. Explicación Detallada de la Lógica del Código**

### **2.1. Ejecución del Script de Descarga**
- **Función `ejecutar_descarga()`**:
  - Esta función ejecuta el script `goes16Download.py` utilizando `subprocess.run()`. Se emplea `check=True` para que, si el script finaliza con un error, se lance una excepción (`CalledProcessError`).
  - **Manejo de Errores**: Si ocurre un error durante la ejecución del script de descarga, se captura la excepción y se imprime un mensaje que describe el fallo. Cabe mencionar que `goes16Download.py` tiene un mecanismo de reconexión que intenta reanudar la descarga automáticamente si hay una pérdida temporal de conexión.

### **2.2. Ejecución del Script de Procesamiento**
- **Función `ejecutar_procesamiento()`**:
  - Ejecuta el script `main.py` del procesador de datos en un bucle continuo. Esto permite que el procesamiento se realice repetidamente, procesando nuevos datos a medida que se descargan.
  - Después de cada ejecución del script de procesamiento, el script espera 60 segundos antes de volver a intentarlo. Esto garantiza que los nuevos archivos descargados tengan tiempo suficiente para ser detectados y procesados adecuadamente.
  - **Manejo de Errores**: Si ocurre un error durante el procesamiento, la excepción se captura e imprime un mensaje que describe el problema. A pesar del error, el bucle continúa, asegurando que se siga intentando el procesamiento en intervalos regulares.

### **2.3. Ejecución Concurrente de Descarga y Procesamiento**
- **Uso de `ThreadPoolExecutor`**:
  - Se utiliza `ThreadPoolExecutor` para ejecutar ambas funciones (`ejecutar_descarga` y `ejecutar_procesamiento`) en paralelo, en diferentes hilos.
  - **Futuros (`future_descarga` y `future_procesamiento`)**: Cada función se ejecuta en un hilo separado, lo cual permite que la descarga de datos y el procesamiento de archivos se realicen simultáneamente. Esto es crucial para evitar cuellos de botella y optimizar el flujo de trabajo.
  - **Sincronización**: Se emplea `concurrent.futures.wait()` para asegurarse de que ambas tareas finalicen. Dado que `ejecutar_procesamiento()` está diseñado con un bucle infinito, la tarea de procesamiento nunca finaliza, lo cual significa que el script continuará funcionando indefinidamente a menos que se detenga manualmente.

---

## **3. Camino de la Información en el Proceso**

1. **Inicio**:
   - El script `run_all.py` se inicia y llama a las funciones `ejecutar_descarga()` y `ejecutar_procesamiento()` usando `ThreadPoolExecutor` para ejecutarlas de manera concurrente.

2. **Descarga de Datos**:
   - La función `ejecutar_descarga()` inicia la descarga de datos satelitales utilizando el script `goes16Download.py`. En caso de fallo en la conexión, el script se reanuda automáticamente.

3. **Procesamiento de Datos**:
   - La función `ejecutar_procesamiento()` monitorea continuamente el directorio de entrada (`inbox`) para detectar y procesar los nuevos archivos descargados. El bucle se asegura de intentar el procesamiento cada 60 segundos.

4. **Ejecución Concurrente**:
   - Ambas funciones (`ejecutar_descarga()` y `ejecutar_procesamiento()`) se ejecutan simultáneamente utilizando hilos, asegurando que el sistema funcione de forma continua y eficiente. Esto permite que la descarga y el procesamiento estén siempre en marcha, sin que uno dependa del otro.

5. **Terminación Manual**:
   - El script está diseñado para ejecutarse indefinidamente hasta que se detenga manualmente (por ejemplo, mediante una interrupción del usuario como `CTRL+C`).

---

## **4. Consideraciones de Diseño**

- **Manejo de Errores Resiliente**:
  - Ambos procesos (`descarga` y `procesamiento`) están diseñados para manejar errores sin detener el script completo. Esto asegura que fallos temporales (como pérdidas de conexión a S3 o problemas de procesamiento) no interrumpan permanentemente el flujo de trabajo.
  
- **Bucle Continuo para el Procesamiento**:
  - La implementación del bucle continuo en el procesamiento permite garantizar que cada nuevo archivo que llega al directorio de entrada sea procesado automáticamente.

- **Sincronización y Ejecución en Paralelo**:
  - Utilizando `ThreadPoolExecutor`, se asegura que la descarga de datos no tenga que esperar al procesamiento, y viceversa. Esto aumenta la eficiencia general del sistema, especialmente en escenarios de gran volumen de datos.

---

## **5. Resumen y Conclusión**

El script `run_all.py` es crucial para la ejecución concurrente de la descarga y el procesamiento de los datos satelitales GOES-16. Permite que ambos procesos se realicen de manera continua, asegurando que siempre haya datos disponibles para análisis sin intervención manual. Su diseño, que utiliza `ThreadPoolExecutor` y la gestión resiliente de errores, permite una operación autónoma y eficiente.

---


