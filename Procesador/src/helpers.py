import numpy as np
import colorsys
import json
import os
from netCDF4 import Dataset
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
from matplotlib.patches import Rectangle
from PIL import Image
import cartopy

Image.MAX_IMAGE_PIXELS = 1000000000

def GetCroppedImage(netCDFread, min_lon, max_lon, min_lat, max_lat):
    """
    Obtiene una imagen recortada de los datos NetCDF en las coordenadas especificadas.

    Args:
        netCDFread (Dataset): Objeto NetCDF leído.
        min_lon (float): Longitud mínima.
        max_lon (float): Longitud máxima.
        min_lat (float): Latitud mínima.
        max_lat (float): Latitud máxima.

    Returns:
        tuple: Extensión de la imagen y los índices de las coordenadas recortadas.
    """
    band_resolution_km = float(getattr(netCDFread, 'spatial_resolution').split("km")[0])
    filepath = os.path.abspath(__file__).split('/src')[0] + '/data/grids/'

    lons = np.loadtxt(filepath + 'g16_lons_8km.txt')
    lats = np.loadtxt(filepath + 'g16_lats_8km.txt')
    ref_grid_resolution_km = 8

    half = int(np.shape(lons)[0] / 2)
    min_lon_idx = (abs(lons - min_lon)[half, :]).argmin()
    max_lon_idx = (abs(lons - max_lon)[half, :]).argmin()
    max_lat_idx = (abs(lats - min_lat)[:, half]).argmin()
    min_lat_idx = (abs(lats - max_lat)[:, half]).argmin()

    frac = int(ref_grid_resolution_km / band_resolution_km)
    min_lat_idx *= frac
    min_lon_idx *= frac
    max_lat_idx *= frac
    max_lon_idx *= frac

    sat_h = netCDFread.variables['goes_imager_projection'].perspective_point_height
    x = netCDFread.variables['x'][min_lon_idx:max_lon_idx] * sat_h
    y = netCDFread.variables['y'][min_lat_idx:max_lat_idx] * sat_h

    img_extent = (x.min(), x.max(), y.min(), y.max())
    img_indexes = [min_lon_idx, max_lon_idx, min_lat_idx, max_lat_idx]

    return img_extent, img_indexes

def GetPlotObject(confData, extent):
    """
    Crea un objeto de trama configurado con los parámetros especificados.

    Args:
        confData (dict): Diccionario de configuración.
        extent (list): Extensión de la trama.

    Returns:
        Axes: Objeto de ejes configurado.
    """
    shapesdir = os.path.dirname(os.path.abspath(__file__)).split('/src')[0] + '/data/shp'
    ax = plt.axes(projection=ccrs.PlateCarree())

    extent = [extent[0], extent[1], extent[2] - 1.0, extent[3]]
    ax.set_extent(extent, ccrs.PlateCarree())

    cartopy.config['pre_existing_data_dir'] = shapesdir
    ax.coastlines('10m', lw=confData['line_width_inches_for_coast'], color='black')

    xlocs = np.arange(-90.0, -45 + 10, 10)
    ylocs = np.arange(-55.5, -15.5 + 10, 10)
    gl = ax.gridlines(xlocs=xlocs, ylocs=ylocs, linestyle='--', color='black', draw_labels=True, linewidth=0.3)
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlabel_style = {'size': 4}
    gl.ylabel_style = {'size': 4}

    shp_dir1 = shapesdir + '/limite_internacional2/ne_10m_admin_0_map_units_PLATE.shp'
    paises = list(shpreader.Reader(shp_dir1).geometries())
    for pais in paises:
        ax.add_geometries([pais], ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=confData['line_width_inches_for_nation_limits'])

    shp_dir2 = shapesdir + '/limite_interprovincial2/008b_limites_provinciales_linea_PLATE.shp'
    provincias = list(shpreader.Reader(shp_dir2).geometries())
    for provincia in provincias:
        ax.add_geometries([provincia], ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=confData['line_width_inches_for_province_limits'])

    return ax

def LoadDictionary(path):
    """
    Carga un diccionario desde un archivo de configuración.

    Args:
        path (str): Ruta del archivo de configuración.

    Returns:
        dict: Diccionario cargado.
    """
    with open(path, 'r') as f:
        content = f.read()
        dic = eval(content)
    return dic

def GetCalibratedImage(netCDFread, image):
    """
    Calibra la imagen utilizando los metadatos disponibles en el archivo NetCDF.

    Args:
        netCDFread (Dataset): Objeto NetCDF leído.
        image (ndarray): Datos de la imagen a calibrar.

    Returns:
        tuple: Imagen calibrada y la unidad de medida correspondiente.
    """
    metaCDF = netCDFread.variables
    icanal = int(metaCDF['band_id'][:])
    if icanal >= 7:
        fk1 = metaCDF['planck_fk1'][0]
        fk2 = metaCDF['planck_fk2'][0]
        bc1 = metaCDF['planck_bc1'][0]
        bc2 = metaCDF['planck_bc2'][0]
        mask = image <= 0
        image_masked = np.ma.masked_array(image, mask=mask)
        image_cal = (fk2 / (np.log((fk1 / image_masked) + 1)) - bc1) / bc2 - 273.15
        unit = 'Temperatura de Brillo [°C]'
    else:
        kappa0 = metaCDF['kappa0'][0]
        image_cal = kappa0 * image
        unit = 'Reflectancia'
    return image_cal, unit

def AddImageFoot(ax, title, institution=None, size=8.0):
    """
    Añade el pie de imagen con el título y la institución opcional.

    Args:
        ax (Axes): Objeto de ejes.
        title (str): Título de la imagen.
        institution (str, optional): Nombre de la institución.
        size (float, optional): Tamaño del texto.

    Returns:
        None
    """
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    width = abs(xlim[0]) + abs(xlim[1])
    height = 0.035 * (abs(ylim[0]) + abs(ylim[1]))
    ax.add_patch(Rectangle((xlim[0], ylim[1]-height), width, height, alpha=1, zorder=3, facecolor='white'))
    ax.text(xlim[0], ylim[1]-height/1.5, title, horizontalalignment='left', color='black', size=size)
    if institution:
        ax.text(xlim[1] - 0.05 * xlim[1], ylim[1] - height / 1.5, institution, horizontalalignment='right', color='black', size=size)

def AddTemperatureLegend(ax):
    """
    Añade la leyenda de temperatura a la imagen.

    Args:
        ax (Axes): Objeto de ejes.

    Returns:
        None
    """
    colors = ['yellow', 'orange', 'red']
    temperature_ranges = [[-53, -63], [-63, -73], [-73, -90]]

def AddLogo(ax):
    """
    Añade el logo de CONAE-Argentina a la imagen.

    Args:
        ax (Axes): Objeto de ejes.

    Returns:
        None
    """
    logo_path = 'Procesador/data/logo/logo.png'  
    logo_img = plt.imread(logo_path)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    logo_width = 0.1 * (xlim[1] - xlim[0])
    logo_height = logo_width * logo_img.shape[0] / logo_img.shape[1]
    logo_x = xlim[1] - 0.01 * (xlim[1] - xlim[0]) - logo_width
    logo_y = ylim[1] - 0.001 * (ylim[1] - ylim[0]) - logo_height - 0.01 * (ylim[1] - ylim[0])
    ax.imshow(logo_img, extent=(logo_x, logo_x + logo_width, logo_y, logo_y + logo_height), aspect='auto', zorder=10)














    









