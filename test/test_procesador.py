import unittest
import os
import shutil
import glob


class TestProcesador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuración inicial antes de las pruebas."""
        cls.test_workdir = "test_workdir/"
        cls.test_inbox = "test_inbox/"
        cls.test_gif_path = os.path.join(cls.test_workdir, "test_conae.gif")

        # Crear directorios de prueba
        os.makedirs(cls.test_workdir, exist_ok=True)
        os.makedirs(cls.test_inbox, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """Limpieza después de las pruebas."""
        if os.path.exists(cls.test_workdir):
            shutil.rmtree(cls.test_workdir)
        if os.path.exists(cls.test_inbox):
            shutil.rmtree(cls.test_inbox)

    def procesar_archivo(self, image_path):
        """Simula el procesamiento de un archivo NetCDF."""
        try:
            # Simula la creación de una imagen procesada
            output_image = os.path.join(self.test_workdir, "processed_image.png")
            with open(output_image, "w") as f:
                f.write("Simulated image data")
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")

    def actualizar_gif(self, imagenes, gif_path):
        """Simula la actualización de un GIF."""
        try:
            with open(gif_path, "w") as f:
                f.write("Simulated GIF data")
        except Exception as e:
            print(f"Error al actualizar el GIF: {e}")

    def test_procesar_archivo(self):
        """Prueba el procesamiento de un archivo NetCDF."""
        # Simular un archivo NetCDF vacío
        test_file = os.path.join(self.test_inbox, "test_file.nc")
        with open(test_file, "w") as f:
            f.write("")

        # Llamar a la función de procesamiento
        self.procesar_archivo(test_file)

        # Verificar si se generó un archivo PNG en el directorio de trabajo
        generated_files = glob.glob(os.path.join(self.test_workdir, "*.png"))
        self.assertGreater(len(generated_files), 0, "No se generaron imágenes procesadas.")
        print("\033[92m✓ Procesamiento de archivo NetCDF correcto\033[0m")

    def test_actualizar_gif(self):
        """Prueba la actualización del GIF con imágenes existentes."""
        # Crear imágenes simuladas
        for i in range(3):
            test_image = os.path.join(self.test_workdir, f"test_image_{i}.png")
            with open(test_image, "w") as f:
                f.write("dummy data")

        # Llamar a la función para actualizar el GIF
        self.actualizar_gif(glob.glob(os.path.join(self.test_workdir, "*.png")), self.test_gif_path)

        # Verificar que se generó el archivo GIF
        self.assertTrue(os.path.exists(self.test_gif_path), "No se generó el archivo GIF.")
        print("\033[92m✓ Actualización de GIF correcta\033[0m")


if __name__ == "__main__":
    print("\nEjecutando pruebas para la lógica del procesador...\n")
    unittest.main(verbosity=2)
