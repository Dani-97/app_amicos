# App Amicos (README).

Este repositorio contiene la implementación de la App Amicos, una aplicación Android
CAA (Comunicación Aumentativa y Alternativa) para la asistencia a personas con
dificultades del habla.

Para la ejecución de la aplicación, se facilita un docker que ya instala las dependencias necesarias. Para poder ejecutar la aplicación, deben seguirse los siguientes pasos:

1. Clonar el repositorio localmente.
2. Ejecutar el script build.sh, que construirá la imagen de docker.
3. Ejecutar el script run.sh, que permitirá el acceso al contenedor de docker que se crea sobre la imagen previamente construida.
4. Ejecutar os.system("python ./src/main.py") dentro del terminal interactivo de Python (importando la librería os).
