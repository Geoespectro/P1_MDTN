### **Revisión y Mejora del Archivo Readme.md**

---

# 🌐 **MDTN v0.1 - Proyecto de Descarga y Procesamiento de Datos Satelitales GOES-16**

**MDTN v0.1** es un sistema diseñado para automatizar la descarga y el procesamiento de datos satelitales **GOES-16**, facilitando la generación de mapas de topes nubosos. Es ideal para usuarios y desarrolladores enfocados en análisis climático, teledetección y meteorología.

---

## 📖 **Descripción General**

El proyecto consta de dos módulos principales:
1. **📥 Descarga de Datos**: Utiliza `goes16Download.py` para descargar imágenes desde el bucket S3 de NOAA.
2. **⚙️ Procesamiento de Datos**: Procesa las imágenes descargadas, aplicando calibraciones y generando productos visuales con `main.py`.

---

## 📂 **Estructura del Proyecto**

```plaintext
.
├── descarga
│   ├── goes16Download.py       # Script principal para descargar imágenes GOES-16
│   ├── helpers.py              # Funciones auxiliares para la descarga
│   └── setup.json              # Configuración de la descarga
├── docs
│   ├── descarga_doc.md         # Documentación del módulo de descarga
│   ├── docs_test               # Documentación de pruebas unitarias
│   │   ├── test_descarga.md    # Pruebas del módulo de descarga
│   │   └── test_procesador.md  # Pruebas del módulo de procesamiento
│   ├── procesador_doc.md       # Documentación del módulo de procesamiento
│   └── run_all_doc.md          # Documentación del script lanzador
├── Procesador
│   ├── data                    # Configuraciones y datos auxiliares (shapefiles, etc.)
│   │   ├── conf                # Configuración de parámetros del procesamiento
│   │   │   └── SMN_dict.conf   # Archivo de configuración principal
│   │   ├── grids               # Archivos de coordenadas
│   │   │   ├── g16_lats_8km.txt
│   │   │   └── g16_lons_8km.txt
│   │   ├── logo                # Recursos gráficos
│   │   │   └── logo.png
│   │   └── shp                 # Shapefiles para la generación de mapas
│   │       ├── limite_internacional2
│   │       ├── limite_interprovincial2
│   │       └── shapefiles
│   │           └── natural_earth/physical
│   ├── inbox                   # Directorio de entrada para las imágenes descargadas
│   ├── main.py                 # Script principal para el procesamiento
│   ├── src                     # Carpeta auxiliar
│   │   └── helpers.py          # Funciones auxiliares del módulo de procesamiento
│   └── workdir                 # Resultados del procesamiento
├── test
│   ├── test_descarga.py        # Pruebas unitarias del módulo de descarga
│   └── test_procesador.py      # Pruebas unitarias del módulo de procesamiento
├── Readme.md                   # Este archivo
├── requirements.txt            # Dependencias del proyecto
├── run_all.py                  # Script lanzador para ejecutar descarga y procesamiento
└── run_all_tk.py               # Versión alternativa con interfaz gráfica
```

---

## 🛠️ **Requisitos del Proyecto**

### **Requisitos del Sistema**:
- **Python 3.8+**

### **Bibliotecas de Python necesarias**:
- `boto3`, `s3fs`, `numpy`, `netCDF4`, `matplotlib`, `cartopy`, `watchdog`, `imageio`, `concurrent.futures`

Instala las dependencias ejecutando:
```bash
pip install -r requirements.txt
```

*Nota*: Es recomendable trabajar en un entorno virtual para mantener organizadas las dependencias del proyecto.

---

## 🚀 **Instrucciones de Uso**

### **1️⃣ Configuración Inicial**
- Edita `descarga/setup.json` para establecer parámetros como:
  - Fecha de inicio y fin.
  - Bandas a descargar.
  - Rutas de almacenamiento.
- Ajusta la configuración de visualización y parámetros geográficos en `Procesador/data/conf/SMN_dict.conf`.

### **2️⃣ Ejecución del Proyecto**
Ejecuta el script principal:
```bash
python run_all.py
```
Esto iniciará simultáneamente los módulos de descarga y procesamiento, permitiendo una operación continua.

Si prefieres una interfaz gráfica, utiliza:
```bash
python run_all_tk.py
```

---

## 📚 **Documentación**

Consulta la documentación específica de cada módulo y pruebas en la carpeta `docs`:
- **Descarga**: [`docs/descarga_doc.md`](docs/descarga_doc.md) - Explica la lógica de descarga y cómo se ejecuta.
- **Procesamiento**: [`docs/procesador_doc.md`](docs/procesador_doc.md) - Describe el módulo de procesamiento.
- **Pruebas Unitarias**: [`docs/docs_test/`](docs/docs_test/) - Documentación detallada sobre las pruebas para descarga y procesamiento.
- **Script Lanzador**: [`docs/run_all_doc.md`](docs/run_all_doc.md) - Explicación del script lanzador que conecta descarga y procesamiento.

---

## ✨ **Mejoras Futuras**

Algunas posibles mejoras incluyen:
- **⚡ Optimización**: Mejorar la lógica de reintentos y el manejo de descargas interrumpidas para garantizar una mayor eficiencia.
- **📢 Notificaciones**: Implementar notificaciones (por ejemplo, por correo electrónico o mensajería instantánea) para alertar sobre errores o finalización de tareas.
- **📊 Visualización**: Añadir dashboards interactivos para explorar los resultados del análisis y procesamiento de imágenes de manera dinámica.

---

## 👫 **Contribuir**

¡Colabora con este proyecto! Sigue estos pasos:
1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y haz commit (`git commit -m 'Descripción del cambio'`).
4. Envía los cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## 📝 **Licencia**

Este proyecto está abierto a la colaboración y se comparte bajo una licencia abierta.

---

## 📩 **Contacto**

Para dudas o sugerencias:
- **Juan Carlos Quinteros**, **Pedro Rivolta**

¡Gracias por utilizar **MDTN v0.1**! Créditos a GOES-16 y los repositorios de AWS.

---




