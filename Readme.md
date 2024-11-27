# MDTN v0.1 - Proyecto de Descarga y Procesamiento de Datos Satelitales GOES-16

## Descripción General

**MDTN v0.1** es un proyecto diseñado para automatizar la descarga y el procesamiento de datos satelitales del satélite **GOES-16**. El sistema descarga imágenes del satélite en tiempo real desde el servidor de NOAA y procesa los datos para generar visualizaciones que permitan un análisis meteorológico y geográfico. Este proyecto está orientado a usuarios y desarrolladores que trabajen en el análisis de datos climáticos, teledetección y estudios meteorológicos.

El proyecto está dividido en dos módulos principales:
1. **Descarga de Datos**: Un módulo para descargar las imágenes satelitales desde el repositorio S3 de NOAA utilizando `goes16Download.py`.
2. **Procesamiento de Datos**: Un módulo para procesar las imágenes descargadas, aplicar calibraciones y generar productos visuales utilizando `main.py`.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
.
├── descarga
│   ├── goes16Download.py       # Script principal para la descarga de imágenes GOES-16
│   ├── helpers.py              # Funciones auxiliares para la descarga
│   ├── setup.json              # Archivo de configuración de la descarga
│   └── doc.md                  # Documentación del módulo de descarga
├── Procesador
│   ├── data                    # Datos auxiliares para el procesamiento (configuración, shapefiles, etc.)
│   ├── inbox                   # Directorio de entrada donde se almacenan las imágenes descargadas
│   ├── main.py                 # Script principal para procesar las imágenes
│   ├── src                     # Código fuente auxiliar para el procesamiento
│   ├── workdir                 # Directorio de trabajo donde se almacenan los resultados del procesamiento
│   └── doc.md                  # Documentación del módulo de procesamiento
├── run_all.py                  # Script lanzador que ejecuta los módulos de descarga y procesamiento concurrentemente
├── doc.md                      # Documentación general del proyecto
└── README.md                   # Este archivo, que proporciona una descripción general del proyecto
```

## Requisitos del Proyecto

Para ejecutar **MDTN v0.1**, necesitarás instalar los siguientes requisitos:
- **Python 3.8+**
- Bibliotecas de Python:
  - `boto3`
  - `s3fs`
  - `numpy`
  - `netCDF4`
  - `matplotlib`
  - `cartopy`
  - `watchdog`
  - `imageio`
  - `concurrent.futures`

Puedes instalar las dependencias con el siguiente comando:
```
pip install -r requirements.txt
```

## Instrucciones de Uso

### 1. Configurar el Proyecto

- Configura las variables en el archivo `setup.json` dentro del directorio `descarga/`. Este archivo define los parámetros para la descarga de imágenes, como la fecha de inicio, las bandas a descargar, y la configuración de las rutas.
- Verifica la configuración de `SMN_dict.conf` dentro del directorio `Procesador/data/conf/` para ajustar los parámetros de visualización y geográficos.

### 2. Ejecutar el Proyecto

- Para iniciar la descarga y el procesamiento de los datos de manera concurrente, ejecuta el script `run_all.py`:
  ```
  python run_all.py
  ```
- El script `run_all.py` lanzará simultáneamente los procesos de descarga y procesamiento. La descarga de datos se ejecutará continuamente y el procesamiento se realizará en intervalos regulares.

## Documentación de los Módulos

Cada módulo del proyecto cuenta con su propia documentación detallada, que puedes encontrar en:
- **Descarga de Datos**: `descarga/doc.md`
- **Procesador de Datos**: `Procesador/doc.md`
- **Script Lanzador**: La documentación del script `run_all.py` está incluida en el archivo `doc.md` en la raíz del proyecto.

## Mejoras y Futuras Actualizaciones

Este proyecto es la versión 0.1 y, por lo tanto, está sujeto a futuras mejoras. Algunas posibles áreas de desarrollo incluyen:
- **Optimización de la Descarga**: Mejorar la lógica de reintento y la capacidad de reanudar descargas de manera más eficiente.
- **Monitoreo Mejorado**: Agregar un sistema de notificaciones que informe al usuario cuando ocurre un error o cuando se completa una tarea.
- **Visualización**: Incorporar paneles de control para una visualización interactiva de los datos procesados.

## Contribuir al Proyecto

Si deseas contribuir al desarrollo del proyecto, por favor, sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios necesarios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Envía tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está abierto a la colaboración.

## Contacto

Para más información, preguntas o sugerencias, no dudes en contactarnos:
- **Compiladores**: Juan Carlos Quinteros, Pedro Rivolta

¡Gracias por utilizar **MDTN v0.1** creditos para Goes-16 y los repsoitorios de AWS!

