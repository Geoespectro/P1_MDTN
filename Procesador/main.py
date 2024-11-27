import os
import json
import time
import src.helpers as goeshelp
import numpy as np
from netCDF4 import Dataset
from datetime import datetime
import matplotlib
import logging
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import imageio
from PIL import Image

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from src.helpers import AddTemperatureLegend, AddLogo, AddImageFoot, GetPlotObject

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configura rutas y leer archivo de configuración
json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/conf/SMN_dict.conf")
confData = goeshelp.LoadDictionary(json_file_path)
workdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), confData['workdir'])
cptdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), confData['cptdir'])
inboxdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), confData['inbox'])
gif_path = os.path.join(workdir, 'conae.gif')

# Crea directorios si no existen
if not os.path.exists(workdir):
    os.makedirs(workdir)
if not os.path.exists(inboxdir):
    os.makedirs(inboxdir)

logging.info(f"Directorio de trabajo: {workdir}")
logging.info(f"Directorio de entrada: {inboxdir}")

def actualizar_gif(imagenes, gif_path):
    """
    Actualiza el GIF con una lista de imágenes y una duración específica entre cuadros usando Pillow.

    :param imagenes: Lista de rutas a las imágenes.
    :param gif_path: Ruta del archivo GIF de salida.
    """
    # Leer la duración desde el archivo de configuración
    frame_duration = confData.get('gif_frame_duration', 1.0)  # Valor predeterminado: 1 segundo
    frame_duration_ms = int(frame_duration * 1000)  # Convertir segundos a milisegundos
    logging.info(f"Configurando duración por cuadro en {frame_duration} segundos.")

    try:
        # Cargar todas las imágenes
        frames = [Image.open(imagen) for imagen in imagenes]

        # Crear el GIF con la duración deseada
        if frames:
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=frame_duration_ms,  # Duración en milisegundos
                loop=0  # Repetir infinitamente
            )
            logging.info(f"GIF generado correctamente: {gif_path}")
        else:
            logging.warning("No se encontraron imágenes para generar el GIF.")
    except Exception as e:
        logging.error(f"Error al generar el GIF: {e}")

def procesar_archivo(image_path):
    """
    Procesa un archivo NetCDF para generar imágenes y actualiza el GIF.

    :param image_path: Ruta del archivo NetCDF.
    """
    try:
        logging.info(f'Procesando archivo {image_path}')
        netCDFread = Dataset(image_path, 'r')
    except Exception as e:
        logging.error(f"Error al leer el archivo NetCDF {image_path}: {e}")
        return

    # Extraer metadatos
    logging.info('Extrayendo metadatos.')
    YY, MM, DD = netCDFread.__dict__['time_coverage_start'].split('T')[0].split('-')
    HH, mm, s_ms = netCDFread.__dict__['time_coverage_start'].split('T')[1].split('Z')[0].split(':')
    ss, mls = s_ms.split('.')

    Tinicio = f'{YY}{MM}{DD}_{HH}{mm}{ss}'

    metaCDF = netCDFread.variables

    # Verificar y obtener la proyección
    if 'geospatial_lat_lon_extent' in metaCDF:
        lon_0 = metaCDF['geospatial_lat_lon_extent'].getncattr('geospatial_lon_center')
    else:
        lon_0 = 0  # Valor predeterminado si no se encuentra

    sat_h = metaCDF['goes_imager_projection'].perspective_point_height

    # Verificar y obtener el canal
    if 'band_id' in metaCDF:
        icanal = int(metaCDF['band_id'][:])
    else:
        icanal = 0  # Valor predeterminado si no existe

    # Definir el extent a generar
    region = 'ARG'
    if region == 'SuA_ARG':
        extent = [confData['sudamerica_lon_W'], confData['sudamerica_lon_E'], confData['sudamerica_lat_S'], confData['sudamerica_lat_N']]
    elif region == 'SuA':
        extent = [confData['sudamerica_lon_W'], confData['sudamerica_lon_E'], confData['sudamerica_lat_S'], confData['sudamerica_lat_N']]
    elif region == 'ARG':
        extent = [confData['argentina_lon_W'], confData['argentina_lon_E'], confData['argentina_lat_S'], confData['argentina_lat_N']]
    elif region == 'test':
        extent = [-68.0, -52.0, -42.0, -31.0]
    else:
        logging.error('Debe seleccionar una de las siguientes áreas: SuA_ARG, SuA, ARG, custom!')
        return

    logging.info('Comienza el procesamiento de los productos IROL para Argentina y Sudamérica.')
    start = time.time()

    # Levanta la imagen recortada y obtener el extent
    logging.info('Lectura de la imagen recortada.')
    img_extent, img_indexes = goeshelp.GetCroppedImage(netCDFread, 
                                extent[0] + confData['delta_lon_W_for_graph'],
                                extent[1],
                                extent[2] + confData['delta_lat_S_for_graph'],
                                extent[3] + confData['delta_lat_N_for_graph'])

    imagedata = netCDFread.variables['Rad'][img_indexes[2]:img_indexes[3],
                                                img_indexes[0]:img_indexes[1]][::1,::1]

    # Calibración de los datos
    image_cal, Unit = goeshelp.GetCalibratedImage(netCDFread, imagedata)
    del imagedata

    # Define los umbrales de temperatura
    thr_1 = -53  # Rango entre -53 y -63 grados
    thr_2 = -63  # Rango entre -63 y -73 grados
    thr_3 = -73  # Rango entre -73 y -90 grados
    thr_min = -90  # Rango mínimo aceptado

    # Asignar NaN a los valores fuera de los rangos establecidos
    image_cal = np.where((image_cal < thr_min) | (image_cal > thr_1), np.nan, image_cal)

    # Clasificación de valores en rangos
    image_class = np.full(image_cal.shape, np.nan)
    image_class = np.where((image_cal >= thr_1), 0, image_class)
    image_class = np.where((image_cal < thr_1) & (image_cal >= thr_2), 1, image_class)
    image_class = np.where((image_cal < thr_2) & (image_cal >= thr_3), 2, image_class)
    image_class = np.where(image_cal < thr_3, 3, image_class)

    # Crear un mapa de colores donde el valor NaN es el fondo blanco
    colors = ['white', 'yellow', 'orange', 'red']
    cmap = matplotlib.colors.ListedColormap(colors)
    cmap.set_bad(color='white')  # Asignar color blanco a los valores NaN

    # Armando las figuras y ejes
    crs = ccrs.Geostationary(central_longitude=lon_0, satellite_height=sat_h)
    fig = plt.figure(clear='True')
    fig.set_size_inches(confData['figure_length_inches'], confData['figure_high_inches'])
    ax = GetPlotObject(confData, extent)

    # Define los colores y los límites de la barra lateral
    colors = ["red", "orange", "yellow"]
    bounds = [-90 , -73, -63, -53]
    norm = matplotlib.colors.BoundaryNorm(bounds, len(colors))

    # Agrega la barra lateral con título y etiquetas personalizadas
    sm = plt.cm.ScalarMappable(cmap=matplotlib.colors.ListedColormap(colors), norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, boundaries=bounds, ticks=bounds, ax=ax)
    cbar.ax.set_title('T°C', fontsize=8)
    cbar.ax.tick_params(labelsize=6)
    cbar.ax.set_yticklabels([f'{int(tick)}°C' for tick in bounds], fontsize=6)

    # Reproyección de los datos con cartopy
    plt.imshow(image_class, transform=crs, extent=img_extent, origin='upper', cmap=cmap, vmin=-0.5, vmax=3.5, aspect='auto')
    AddTemperatureLegend(ax)

    # Creando las imágenes
    canal = ('%02d' % icanal)
    if region == 'ARG':
        Title = f'GOES-16 ABI Canal {canal} - Mapa de Topes Nubosos {YY}/{MM}/{DD} {HH}:{mm}:{ss} UTC'
        nombre_base = f'CONAE_PRD_GOES16_ABI_IROL_{YY}{MM}{DD}_{HH}{mm}{ss}{mls}00_'
        AddImageFoot(ax, Title, size=8.0)
        AddLogo(ax)
        nombre_completo = nombre_base + 'gCArgentina_v001'
        png_dir = os.path.join(workdir, nombre_completo + '.png')
        plt.savefig(png_dir, dpi=confData['figure_resolution_dpi'])
        logging.info(f"Imagen guardada en {png_dir}")
        
        # Actualizar el GIF con la nueva imagen
        imagenes_existentes = sorted(glob.glob(os.path.join(workdir, 'CONAE_PRD_GOES16_ABI_IROL_*.png')))
        actualizar_gif(imagenes_existentes, gif_path)

# Monitoreo de la carpeta inbox usando watchdog
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.nc'):
            procesar_archivo(event.src_path)


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, inboxdir, recursive=False)
    observer.start()

    logging.info("Monitor de archivos iniciado.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


