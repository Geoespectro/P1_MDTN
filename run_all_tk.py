# NOTA IMPORTANTE:
# Esta es una interfaz gráfica en fase de desarrollo que tiene como objetivo 
# realizar las mismas tareas que el script `ru_all.py`, pero con una experiencia 
# más interactiva y controlada. La aplicación permite al usuario:
# 
# 1. Configurar las fechas y horas para las operaciones de descarga y procesamiento.
# 2. Iniciar, pausar y reanudar la descarga de datos de GOES-16.
# 3. Supervisar y gestionar el estado de ambos procesos desde una sola ventana.
#
# Por el momento, el diseño y las funcionalidades son básicos y podrían contener errores. 
# El propósito principal de esta versión es probar la integración de la interfaz con 
# los procesos subyacentes y recopilar comentarios para mejorar.
#
# ¡Cualquier sugerencia o reporte de problemas será bienvenido para futuras versiones!


import subprocess
import tkinter as tk
from tkinter import messagebox
import threading
import time
import json
import os

# Variables globales para controlar el estado de los procesos
procesos_activos = {
    "descarga": None,
    "procesamiento": None,
}

# Ruta del archivo de configuración
setup_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'descarga/setup.json')

# Funciones para actualizar el estado en la interfaz
def actualizar_estado(texto):
    """
    Actualiza la etiqueta de estado en la interfaz gráfica y también imprime el estado en la consola.

    Args:
        texto (str): El estado actual a mostrar en la interfaz y la consola.
    """
    etiqueta_estado.config(text=f"Estado: {texto}")
    print(texto)  # Impresión en consola para seguimiento

# Función para actualizar el archivo setup.json con las fechas y horas especificadas
def actualizar_setup_json(start_date, start_time, end_date, end_time):
    """
    Actualiza el archivo de configuración 'setup.json' con las fechas y horas especificadas por el usuario.

    Args:
        start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        start_time (str): Hora de inicio en formato 'HH:MM'.
        end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.
        end_time (str): Hora de fin en formato 'HH:MM'.
    """
    with open(setup_path, 'r') as f:
        setup_data = json.load(f)

    setup_data['dates'] = [start_date] if start_date else setup_data['dates']
    setup_data['start_hour'] = start_time if start_time else setup_data['start_hour']
    setup_data['end_date'] = end_date if end_date else None
    setup_data['end_hour'] = end_time if end_time else None

    with open(setup_path, 'w') as f:
        json.dump(setup_data, f, indent=4)

# Función para ejecutar el script de descarga
def ejecutar_descarga():
    """
    Ejecuta el script de descarga 'goes16Download.py' y actualiza el estado en la interfaz.
    Si ocurre un error, se muestra un mensaje de error en la interfaz gráfica.
    """
    try:
        actualizar_estado("Descarga en ejecución")
        procesos_activos["descarga"] = subprocess.Popen(['python', 'descarga/goes16Download.py'])
        procesos_activos["descarga"].wait()
        actualizar_estado("Descarga finalizada")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante la descarga: {e}")
        actualizar_estado("Error en descarga")

# Función para ejecutar el script de procesamiento
def ejecutar_procesamiento():
    """
    Ejecuta el script de procesamiento 'main.py' y actualiza el estado en la interfaz.
    Si ocurre un error, se muestra un mensaje de error en la interfaz gráfica.
    """
    try:
        actualizar_estado("Procesamiento en ejecución")
        procesos_activos["procesamiento"] = subprocess.Popen(['python', 'Procesador/main.py'])
        procesos_activos["procesamiento"].wait()
        actualizar_estado("Procesamiento finalizado")
    except Exception as e:
        messagebox.showerror("Error", f"Error durante el procesamiento: {e}")
        actualizar_estado("Error en procesamiento")

# Función para iniciar la descarga y el procesamiento
def iniciar_procesos():
    """
    Inicia los procesos de descarga y procesamiento en hilos separados.
    Valida las fechas y horas ingresadas por el usuario antes de iniciar los procesos.
    """
    start_date = entry_start_date.get()
    start_time = entry_start_time.get()
    end_date = entry_end_date.get()
    end_time = entry_end_time.get()
    
    # Validar fechas y horas
    if start_date and start_time:
        try:
            time.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Fecha/hora de inicio inválida")
            return
    if end_date and end_time:
        try:
            time.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Fecha/hora de fin inválida")
            return

    # Actualizar setup.json con los valores de la interfaz
    actualizar_setup_json(start_date, start_time, end_date, end_time)

    # Iniciar los procesos en hilos separados
    if procesos_activos["descarga"] is None:
        threading.Thread(target=ejecutar_descarga, daemon=True).start()
    if procesos_activos["procesamiento"] is None:
        threading.Thread(target=ejecutar_procesamiento, daemon=True).start()

    actualizar_estado("Procesos en ejecución")
    btn_control.config(text="Pausar Descarga", command=pausar_descarga)

# Función para pausar la descarga (sin pausar el procesamiento)
def pausar_descarga():
    """
    Pausa el proceso de descarga si está en ejecución, dejando el proceso de procesamiento activo.
    """
    if procesos_activos["descarga"] and procesos_activos["descarga"].poll() is None:
        # Pausar implica detener el proceso de descarga
        procesos_activos["descarga"].terminate()
        procesos_activos["descarga"] = None
        actualizar_estado("Descarga en pausa, procesamiento en ejecución")
        messagebox.showinfo("Información", "La descarga ha sido pausada. El procesamiento continuará con las imágenes en la carpeta 'Inbox'.")
    btn_control.config(text="Reanudar Descarga", command=reanudar_descarga)

# Función para reanudar la descarga
def reanudar_descarga():
    """
    Reanuda el proceso de descarga que fue previamente pausado y actualiza el estado en la interfaz.
    """
    # Iniciar el proceso de descarga nuevamente
    threading.Thread(target=ejecutar_descarga, daemon=True).start()
    actualizar_estado("Reanudando descarga, procesamiento en ejecución")
    btn_control.config(text="Pausar Descarga", command=pausar_descarga)

# Función para finalizar los procesos
def finalizar_procesos():
    """
    Finaliza ambos procesos (descarga y procesamiento) si están en ejecución y actualiza la interfaz.
    """
    if procesos_activos["descarga"]:
        procesos_activos["descarga"].terminate()
        procesos_activos["descarga"] = None
    if procesos_activos["procesamiento"]:
        procesos_activos["procesamiento"].terminate()
        procesos_activos["procesamiento"] = None
    actualizar_estado("Descarga en pausa, procesamiento en ejecución")
    messagebox.showinfo("Información", "Los procesos han sido finalizados.")
    btn_control.config(text="Iniciar Procesos", command=iniciar_procesos)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("MDTN v0.1 - Control de Descarga y Procesamiento")

# Etiquetas y campos de entrada
tk.Label(root, text="Fecha de Inicio (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
entry_start_date = tk.Entry(root)
entry_start_date.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Hora de Inicio (HH:MM):").grid(row=1, column=0, padx=10, pady=5)
entry_start_time = tk.Entry(root)
entry_start_time.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Fecha de Fin (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
entry_end_date = tk.Entry(root)
entry_end_date.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Hora de Fin (HH:MM):").grid(row=3, column=0, padx=10, pady=5)
entry_end_time = tk.Entry(root)
entry_end_time.grid(row=3, column=1, padx=10, pady=5)

# Botón de control dinámico
btn_control = tk.Button(root, text="Iniciar Procesos", command=iniciar_procesos)
btn_control.grid(row=4, column=0, columnspan=2, pady=10)

# Botón para finalizar los procesos
btn_finalizar = tk.Button(root, text="Finalizar", command=finalizar_procesos)
btn_finalizar.grid(row=5, column=0, columnspan=2, pady=10)

# Etiqueta de estado
etiqueta_estado = tk.Label(root, text="Estado: Inactivo")
etiqueta_estado.grid(row=6, column=0, columnspan=2, pady=10)

# Iniciar el bucle principal de la interfaz
root.mainloop()





