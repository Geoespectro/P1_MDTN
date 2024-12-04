import subprocess
import concurrent.futures 
import time

# Función para ejecutar el script de descarga
def ejecutar_descarga():
    """
    Ejecuta el script de descarga 'goes16Download.py' utilizando subprocess.
    
    Si ocurre un error durante la ejecución, se imprime un mensaje de error.

    Returns:
        None
    """
    try:
        subprocess.run(['python', 'descarga/goes16Download.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error durante la descarga: {e}")

# Función para ejecutar el script de procesamiento
def ejecutar_procesamiento():
    """
    Ejecuta el script de procesamiento 'main.py' en un bucle continuo, esperando 60 segundos entre cada ejecución.
    
    Si ocurre un error durante la ejecución, se imprime un mensaje de error.

    Returns:
        None
    """
    while True:  # Bucle continuo
        try:
            subprocess.run(['python', 'Procesador/main.py'], check=True)
            time.sleep(60)  # Espera de 60 segundos antes de la siguiente ejecución
        except subprocess.CalledProcessError as e:
            print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    """
    Punto de entrada principal del script. Ejecuta la descarga y el procesamiento de imágenes concurrentemente.
    
    Utiliza ThreadPoolExecutor para ejecutar ambas funciones en paralelo.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Ejecutar la descarga y el procesamiento concurrentemente
        future_descarga = executor.submit(ejecutar_descarga)
        future_procesamiento = executor.submit(ejecutar_procesamiento)

        # Esperar a que ambas tareas se completen
        concurrent.futures.wait([future_descarga, future_procesamiento])


















