# Documentación del Módulo de Procesamiento GOES-16

## 1. Descripción General del Módulo

El módulo `main.py` del procesador tiene como objetivo procesar los archivos NetCDF descargados del satélite GOES-16. Utiliza diversas herramientas de visualización y análisis para generar imágenes de los datos, añadiendo leyendas, logos y otros elementos de información. Además, el procesador está configurado para crear un GIF a partir de las imágenes generadas.

Este módulo está diseñado para funcionar de forma automatizada, procesando archivos a medida que se detectan en una carpeta específica, lo cual permite mantener el flujo de información actualizado en tiempo real.

## 2. Explicación Detallada de la Lógica del Código

### 2.1. Configuración y Lectura del Archivo de Configuración
- **Archivo de Configuración (`SMN_dict.conf`)**: Se utiliza para definir parámetros como resolución de imágenes, extensión geográfica, tamaño de etiquetas, entre otros. La configuración se carga al inicio del script para asegurarse de que todas las variables necesarias estén disponibles durante el procesamiento.
- **Lectura del Archivo**: `goeshelp.LoadDictionary(json_file_path)` se encarga de cargar el archivo de configuración. Los valores leídos se almacenan en la variable `confData` para ser utilizados en las funciones posteriores.

### 2.2. Verificación y Creación de Directorios
- **Directorio de Trabajo (`workdir`)**: Es el directorio donde se guardan los resultados del procesamiento, como las imágenes generadas y el GIF.
- **Directorio de Entrada (`inboxdir`)**: Es el directorio donde se colocan los archivos NetCDF descargados para ser procesados.
- **Verificación de Existencia**: El script verifica si los directorios de trabajo y entrada existen, y los crea en caso de que no. Esto se asegura mediante `os.makedirs()` para evitar problemas de falta de rutas al momento de guardar archivos.

### 2.3. Procesamiento Automático de Archivos Nuevos
- **Monitoreo de Directorios con `watchdog`**: Se utiliza la biblioteca `watchdog` para monitorear el directorio `inboxdir`. Cada vez que se detecta un nuevo archivo NetCDF, la función `procesar_archivo()` se llama automáticamente.
- **Clase `MyHandler`**: Define el comportamiento a seguir cuando se detecta un archivo nuevo, permitiendo que el procesamiento ocurra de manera automática sin intervención manual.

### 2.4. Procesamiento de Archivos NetCDF
- **Carga del Archivo**: La función `procesar_archivo(image_path)` se encarga de leer los datos del archivo NetCDF utilizando `Dataset` de la biblioteca `netCDF4`.
- **Extracción de Metadatos**: Se extraen los metadatos necesarios, como la fecha y hora de cobertura del archivo (`time_coverage_start`), que se utilizan para etiquetar las imágenes generadas.
- **Generación de Imágenes Recortadas**: Se utiliza la función `GetCroppedImage()` para recortar la imagen a la región de interés (Argentina o Sudamérica) según la configuración definida.
- **Calibración de la Imagen**: Se emplea `GetCalibratedImage()` para transformar los datos brutos del satélite en valores de temperatura o reflectancia, según el canal del satélite.

### 2.5. Creación de Mapas e Imágenes
- **Uso de `matplotlib` y `cartopy`**: Se utiliza `matplotlib` para generar las figuras y `cartopy` para manejar la proyección y agregar elementos cartográficos como las líneas de costa y fronteras.
- **Agregar Leyendas y Logos**: 
  - **Leyendas**: La función `AddTemperatureLegend()` se usa para añadir una leyenda de temperatura al gráfico.
  - **Logo**: `AddLogo()` añade el logo de CONAE a cada imagen generada para dar crédito a la institución productora de los datos.

### 2.6. Creación del GIF
- **Función `actualizar_gif()`**: Después de generar cada nueva imagen, se actualiza el GIF en el directorio de trabajo. Se utiliza la biblioteca `imageio` para agregar nuevas imágenes al GIF existente.
- **Parámetros del GIF**: Las imágenes se añaden al GIF con una duración de 5 segundos por cuadro, y el GIF se configura para que se reproduzca en un bucle infinito.

### 2.7. Manejo de Logs y Errores
- **Configuración del Logger**: Se utiliza el módulo `logging` para registrar eventos importantes y errores. El formato del log incluye la fecha y hora, el nivel de severidad y el mensaje.
- **Niveles de Log**: Se utilizan diferentes niveles de logs (`INFO`, `ERROR`) para categorizar los eventos. Los registros se imprimen en la consola para facilitar el monitoreo del proceso.

## 3. Camino de la Información en el Proceso de Datos
1. **Inicio**: El script se inicia y se carga la configuración desde `SMN_dict.conf`.
2. **Preparación**: Se verifican y crean los directorios de trabajo necesarios.
3. **Monitoreo de Directorios**: `watchdog` se encarga de monitorear el directorio `inboxdir` para detectar nuevos archivos NetCDF.
4. **Procesamiento de Archivos**:
   - Cada archivo detectado es procesado por `procesar_archivo()`, donde se extraen los datos y se genera la imagen.
   - Se utiliza `matplotlib` para crear el mapa y se añaden elementos como leyendas y logos.
5. **Actualización del GIF**: Las nuevas imágenes generadas se agregan al GIF, manteniéndolo actualizado.
6. **Finalización**: El script sigue monitoreando el directorio hasta que se cierra manualmente.

## 4. Áreas en las que se podria Mejorar el Código
- **Seguridad del Archivo de Configuración**: Reemplazar `eval()` con un formato más seguro como JSON o YAML para evitar riesgos de seguridad.
- **Optimización del Uso de Memoria**: Procesar los datos en chunks para evitar problemas de memoria si los archivos NetCDF son demasiado grandes.
- **Mejora de la Visualización**: Optimizar las proyecciones de los mapas y ajustar las leyendas dinámicamente para hacer los gráficos más atractivos y comprensibles.
- **Gestión del Observador de `watchdog`**: Mejorar la robustez del observador para asegurar que continúe funcionando incluso si ocurre un error inesperado.
- **Creación de GIFs**: Configurar el número de imágenes y la resolución para evitar que el archivo GIF se vuelva demasiado grande, lo cual podría afectar el rendimiento.