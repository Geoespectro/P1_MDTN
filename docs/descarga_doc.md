# **Guía Explicativa del Módulo de Descarga GOES-16**

## **1. Descripción General del Proceso de Descarga**

El módulo `goes16Download.py` tiene como objetivo descargar datos satelitales del satélite GOES-16 desde un bucket S3 de la NOAA. Este proceso está diseñado para ser robusto, permitiendo tanto la descarga continua de datos en tiempo real como la descarga de periodos específicos de datos históricos.

La lógica del módulo de descarga se estructura de la siguiente forma:
1. **Configuración Inicial**: Se lee un archivo de configuración (`setup.json`) que contiene los parámetros necesarios para ejecutar el proceso, como fechas, bandas, y configuraciones de directorios.
2. **Verificación y Creación de Directorios**: Se crean las carpetas necesarias para almacenar los datos descargados, registros (`logs`), y una base de datos (`download_db.json`) que permite llevar un control de las descargas.
3. **Conexión y Manejo de la Base de Datos de Descarga**: Se establece una conexión con el servidor S3 y se verifica o inicializa el archivo de base de datos de descargas para reanudar el proceso desde donde se dejó previamente.
4. **Bucle Principal de Descarga**: Utiliza un bucle para recorrer cada hora entre la fecha de inicio y de fin, realizando la descarga de las imágenes correspondientes para cada banda.
5. **Paralelismo**: Emplea `ThreadPoolExecutor` para realizar descargas paralelas de archivos, mejorando la eficiencia y velocidad del proceso.
6. **Registro y Recuperación de Errores**: Los errores y excepciones se registran en un archivo de log, facilitando la detección de problemas y la recuperación del proceso en caso de fallos.

---

## **2. Explicación Detallada de Cada Parte del Código**

### **2.1. Configuración Inicial**
- **Archivo de Configuración (`setup.json`)**: Se carga para definir los parámetros de descarga como:
  - **Fechas de descarga** (`dates`, `end_date`, `start_hour`, `end_hour`).
  - **Bandas a descargar** (`bands`).
  - **Rutas de carpetas** para almacenar imágenes, registros y bases de datos (`image_path`, `db_path`, `log_path`).
- **Lectura del Archivo**: `help.readJson(setup_file)` se usa para leer `setup.json` y almacenar los datos en la variable `data`. Con esto, se configuran variables importantes como las rutas de almacenamiento y las bandas a descargar.

### **2.2. Verificación y Creación de Directorios**
- El script verifica la existencia de los directorios requeridos (`image_path`, `temp_path`, `db_path`, `log_path`) y los crea si no existen mediante `os.makedirs()`. Esto asegura que no se produzcan errores al intentar guardar archivos en directorios inexistentes.

### **2.3. Configuración del Logger**
- Se utiliza `help.createLogger()` para configurar un `logger` que registra mensajes importantes y errores del proceso en un archivo de log.
- **Uso del Logger**: Proporciona visibilidad del proceso de descarga y facilita el monitoreo y depuración del mismo.

### **2.4. Conexión a S3**
- **Conexión Anónima con S3**: Se configura el acceso anónimo al bucket de NOAA con `s3fs.S3FileSystem(anon=True)`. Un bucle `while` se encarga de verificar la conexión y reintentar en caso de fallos.
- **Base de Datos de Descarga (`download_db.json`)**: Se lee o se inicializa si está corrupto o no existe. Esta base de datos lleva el control de qué archivos ya se han descargado.

### **2.5. Bucle Principal de Descarga**
- **Inicio del Bucle**: Comienza en `last_time` si hay una descarga previa o en `start_datetime` si es la primera vez que se ejecuta.
- **Iteración por Fechas y Horas**: Se iteran las fechas y horas, y se obtienen las rutas remotas de las imágenes mediante `help.getRemotePath()`. La descarga de imágenes se realiza para cada banda especificada en `bands`.

### **2.6. Funciones Específicas**
- **`download_file(f, temp_path, final_path, year, day, hour)`**:
  - Descarga un archivo desde la ruta remota `f` y lo guarda temporalmente en `temp_path` antes de moverlo a `final_path`, para asegurar su integridad.
  - **Control de Errores**: Verifica el tamaño del archivo descargado y maneja posibles fallos. Los archivos descargados se mueven a `image_path` solo si la descarga es exitosa.
  - **Actualización de la Base de Datos**: Si la descarga es exitosa, se actualiza `download_db` y se guarda en `download_db.json` para mantener un registro consistente.

- **`get_last_downloaded_time()`**:
  - Devuelve la última fecha y hora de descarga exitosa para continuar el proceso sin necesidad de volver a empezar desde cero.
  - **Recorrido de la Base de Datos**: Recorre `download_db` para encontrar el último conjunto completo de descargas.

### **2.7. Descargas Paralelas**
- **`ThreadPoolExecutor`**:
  - Utiliza `ThreadPoolExecutor` para gestionar las descargas de archivos en paralelo, lo cual acelera el proceso.
  - **Manejo de Excepciones**: Se capturan excepciones de cada hilo mediante `future.result()`. Si hay un error, se registra, pero los otros hilos continúan con la descarga.

### **2.8. Ciclo Continuo y Tiempos de Espera**
- **Lógica de Tiempo de Espera**:
  - **Descargas Futuras**: Si los archivos para una hora específica aún no están disponibles, se mantiene un bucle que los busca hasta que aparezcan. Esto es útil en un entorno de descarga en tiempo real.
  - **Aumento del Tiempo de Espera**: Si un archivo tarda mucho en estar disponible, el tiempo de espera se incrementa progresivamente para reducir la carga en el servidor.

### **2.9. Finalización del Proceso**
- El bucle principal se detiene al alcanzar la fecha de fin (`end_datetime`) o sigue indefinidamente si el script está configurado para la descarga continua.
- **Mensaje Final**: Se imprime un mensaje indicando que el proceso de descarga ha finalizado.

---

## **3. Camino de la Información en el Proceso de Descarga**
1. **Inicio**: El script se inicia y lee la configuración desde `setup.json`.
2. **Preparación**: Se configuran los directorios necesarios y se establece el logger para registrar eventos.
3. **Conexión con S3**: Se verifica la conexión con el bucket de NOAA.
4. **Bucle de Descarga**:
   - Itera sobre las horas y fechas configuradas o en modo continuo.
   - Para cada hora:
     - Obtiene la lista de archivos disponibles en S3.
     - Usa `ThreadPoolExecutor` para descargar los archivos en paralelo.
     - Actualiza la base de datos `download_db` con cada archivo descargado.
5. **Finalización**: El proceso se detiene al alcanzar la fecha y hora de fin o sigue indefinidamente si está en modo de descarga continua.

---

## **4. Áreas en las que se Podria Mejorar el Código **
- **Manejo de Conexiones y Tiempos de Espera**: Se podría optimizar el tiempo de espera entre intentos fallidos para hacer más eficiente la conexión y minimizar el tiempo inactivo.
- **Verificación de la Integridad de los Archivos**: Implementar una verificación de checksum o hash para asegurar que los archivos descargados no estén corruptos.
- **Escalabilidad del Paralelismo**: Ajustar dinámicamente `max_workers` según los recursos disponibles del sistema podría mejorar la eficiencia del proceso de descarga.
- **Modularización**: Dividir lógicas complejas en funciones más pequeñas y reutilizables mejoraría la mantenibilidad del código.
- **Manejo de Logs**: Diferenciar entre distintos niveles de log (INFO, WARNING, ERROR) ayuda a categorizar los eventos de manera más efectiva, facilitando la búsqueda de problemas críticos.

---

