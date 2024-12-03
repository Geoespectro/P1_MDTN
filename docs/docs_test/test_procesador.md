## **Documentación del Test: Procesador**

### **Descripción General**
Este test está diseñado para validar la lógica básica de las funciones principales del procesador:
- **Procesar archivos NetCDF**: Simula la creación de imágenes procesadas.
- **Actualizar un GIF**: Simula la combinación de imágenes procesadas en un archivo GIF.

El test es autónomo y no depende de datos reales ni configuraciones externas, lo que lo hace ideal para pruebas rápidas y portables.

---

### **Estructura del Test**

#### **Directorios de Prueba**
El test crea dos carpetas temporales para realizar sus operaciones:
1. `test_workdir`: Directorio de trabajo donde se generan las imágenes procesadas y el GIF.
2. `test_inbox`: Directorio donde se colocan los archivos `.nc` simulados para el procesamiento.

Ambos directorios son eliminados al finalizar las pruebas.

---

### **Funciones Probadas**

#### **1. `procesar_archivo(image_path)`**
- **Descripción**: 
  Simula el procesamiento de un archivo NetCDF y genera una imagen PNG en el directorio de trabajo.
- **Entrada**: Ruta del archivo NetCDF (simulado).
- **Salida**: Archivo PNG (`processed_image.png`) en `test_workdir`.

#### **2. `actualizar_gif(imagenes, gif_path)`**
- **Descripción**: 
  Simula la actualización de un archivo GIF con una lista de imágenes.
- **Entrada**:
  - `imagenes`: Lista de rutas a imágenes PNG.
  - `gif_path`: Ruta de salida para el archivo GIF.
- **Salida**: Archivo GIF (`test_conae.gif`) en `test_workdir`.

---

### **Casos de Prueba**

#### **1. Test: `test_procesar_archivo`**
- **Propósito**: 
  Verificar que la función `procesar_archivo` genere correctamente una imagen procesada.
- **Método**:
  1. Crea un archivo `.nc` vacío en `test_inbox`.
  2. Llama a `procesar_archivo`.
  3. Comprueba si se generó un archivo PNG en `test_workdir`.
- **Resultado Esperado**: 
  Al menos un archivo PNG generado en `test_workdir`.

#### **2. Test: `test_actualizar_gif`**
- **Propósito**: 
  Validar que la función `actualizar_gif` genere correctamente un archivo GIF combinando varias imágenes.
- **Método**:
  1. Crea imágenes simuladas (`test_image_0.png`, `test_image_1.png`, `test_image_2.png`) en `test_workdir`.
  2. Llama a `actualizar_gif` con estas imágenes.
  3. Comprueba si se generó un archivo GIF en `test_workdir`.
- **Resultado Esperado**: 
  Un archivo GIF (`test_conae.gif`) generado en `test_workdir`.

---

### **Configuración**

#### **Requisitos Previos**
- **Python 3.x**: Asegúrate de tener Python instalado.
- **Bibliotecas estándar**: El test solo utiliza módulos estándar de Python, como `unittest`, `os`, `shutil` y `glob`.

#### **Ejecución del Test**
1. Guarda el archivo del test como `test_procesador.py`.
2. Coloca el archivo en la carpeta deseada.
3. Ejecuta el test con el siguiente comando:
   ```bash
   python test_procesador.py
   ```

---

### **Resultados Esperados**

Si las pruebas son exitosas, deberías ver una salida como esta:

```plaintext
Ejecutando pruebas para la lógica del procesador...

test_actualizar_gif (__main__.TestProcesador)
Prueba la actualización del GIF con imágenes existentes. ... ✓ Actualización de GIF correcta
ok
test_procesar_archivo (__main__.TestProcesador)
Prueba el procesamiento de un archivo NetCDF. ... ✓ Procesamiento de archivo NetCDF correcto
ok

----------------------------------------------------------------------
Ran 2 tests in 0.011s

OK
```

---

### **Notas Importantes**

1. **Datos Simulados**:
   - Este test utiliza datos simulados (archivos vacíos y datos ficticios).
   - No valida el contenido de las imágenes o del GIF generado, solo verifica su creación.

2. **Extensiones Futuras**:
   - Puedes extender este test para trabajar con datos reales.
   - Verifica los contenidos generados comparándolos con resultados esperados.

---

### **Conclusión**
Este test es una solución sencilla y efectiva para validar la lógica básica del procesador. Al ser autónomo, es fácil de mantener y ejecutar en cualquier entorno sin dependencias externas.

--- 

