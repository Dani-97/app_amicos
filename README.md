# App Amicos (README)

Este repositorio contiene la implementación de la App Amicos, una aplicación Android CAA (Comunicación Aumentativa y Alternativa) para la asistencia a personas con dificultades del habla.

## Detalles de la implementación: librerías y herramientas necesarias

La aplicación está implementada con las librerías Kivy y KivyMD, las cuales permiten desarrollar aplicaciones multiplataforma. En el caso de este proyecto, ha sido utilizado porque permite implementar aplicaciones de Android utilizando Python. A pesar de las ventajas, la compilación de las aplicaciones Android con este entorno de desarrollo se complica, ya que es necesario utilizar una herramienta que convierta código Python a código ejecutable por un dispositivo Android. Esto se consigue por medio de la herramienta automatizada Buildozer. En términos generales, la aplicación se puede ejecutar en un dispositivo de escritorio directamente (siempre y cuando no tenga funcionalidades que dependan de la plataforma) haciendo una llamada a "python3 main.py", como en cualquier código de Python habitual. Sin embargo, para poder ejecutar la aplicación móvil, es necesario pasar por el proceso de compilarla con la herramienta Buildozer.

## Desarrollo de la aplicación

Para el desarrollo de la aplicación, en el presente repositorio se facilita un docker que ya instala todo lo necesario para poder ejecutar o compilar la aplicación, proporcionando un entorno de Ubuntu 25.04. Por cuestiones derivadas del uso de Buildozer, se ha configurado este entorno con Python3.11.5, el cual se descarga y se compila durante la creación de la imagen de docker (todo este proceso está completamente automatizado gracias al Dockerfile). Cabe destacar que, a la hora de ejecutar la aplicación en el dispositivo de escritorio, es necesario dar permisos de acceso al contenedor de docker para que pueda utilizar el servidor X11. Esto está resuelto por el script run.sh, que utiliza un binding para proporcionar este acceso. Aun así, es posible que en algunos dispositivos haya que ejecutar la siguiente línea <code>xhost +local:</code> para otorgar esos permisos completamente (no en el contenedor de docker, si no en la máquina local, para permitir que el contenedor pueda hacer uso del servidor X11).

## Ejecución de la aplicación en el dispositivo de escritorio (si no hay dependencias de la plataforma Android)

Para poder ejecutar la aplicación, deben seguirse los siguientes pasos:

1. Clonar el repositorio localmente.
2. Ejecutar el script build.sh, que construirá la imagen de docker.
3. Ejecutar el script run.sh, que permitirá el acceso al contenedor de docker que se crea sobre la imagen previamente construida.
4. Cambiar a la carpeta "src" y ejecutar <code>python3 main.py</code>.

## Ejecución de la aplicación en el dispositivo Android

1. Clonar el repositorio localmente.
2. Ejecutar el script build.sh, que construirá la imagen de docker.
3. Ejecutar el script run.sh, que permitirá el acceso al contenedor de docker que se crea sobre la imagen previamente construida.
4. Cambiar a la carpeta "src" y ejecutar <code>bash create_debug_apk.sh</code>.
5. Esperar a que el proceso de compilación con buildozer se ejecute y construya el APK.
6. Instalar el APK en el dispositivo.

El script <code>create_debug_apk.sh</code> ejecuta buildozer, utilizando para ello la configuración del fichero buildozer.spec y con el código contenido dentro de src. Cabe destacar que la primera ejecución del proceso de compilación será de muy larga duración (puede llegar a ser superior a los 10 minutos) aunque posteriores builds serán mucho más rápidas y llevarán menos de un minuto. A raíz de esta compilación, se crea un directorio .buildozer que almacena todo lo que Buildozer necesita. En otras palabras, la eliminación de ese directorio supone que el proceso de compilación tenga que comenzar desde cero y, por lo tanto, volver a necesitar de un proceso de larga duración para compilar la aplicación por primera vez.

Una vez la aplicación APK haya sido creada, esta se almacenará en la carpeta bin (la cual se crea automáticamente dentro de src). La instalación de esta aplicación seguirá el proceso tradicional de cualquier otra APK, teniendo en cuenta que, debido a que se trata de una aplicación de terceros que no procede de una App Store confiable, los sistemas de seguridad de Android lanzarán múltiples advertencias de que la aplicación podría no ser segura, como es habitual en este tipo de situaciones. Sin embargo, dado que es una aplicación de origen fiable, estas advertencias no se deben tener en cuenta para este caso en particular.

<code>Recomendación: para instalar la aplicación en el emulador, es tan sencillo como soltar el fichero de la APK desde el explorador de archivos del ordenador a la pantalla principal.</code>

## Depuración de la aplicación en el dispositivo Android

El proceso de depuración, cuando se trabaja con un dispositivo Android, es tediosa ya que no existe un depurador que permita añadir breakpoints y debe hacerse por medio de loggings (lo cual puede conseguirse por medio de prints en el código de Python). Los loggings relevantes de la aplicación se podrán obtener con la aplicación adb logcat, el sistema predeterminado que utiliza Android para depurar sus dispositivos. En concreto, para poder filtrar aquellos logs que tienen que ver directamente con la aplicación, debe ejecutarse la siguiente línea <code>adb logcat | grep python</code>. En caso de que se produzca un error de ejecución en la aplicación, debería poder visualizarse de esta forma.

## Consideraciones sobre Buildozer

Buildozer es una herramienta que automatiza el proceso de compilación y, como tal, su configuración debe ser muy precisa para que dicha compilación se realice de forma satisfactoria. Aquí se describen algunos detalles relevantes para explicar correctamente qué significan las líneas más importantes en el fichero de configuración <code>buildozer.spec</code>:

- **title**: título de la aplicación. Es el texto que aparecerá junto al icono una vez que dicha aplicación se instale.

- **package_name** y **package_domain**: el nombre de paquete habitual en implementaciones de Java (y, por consiguiente, de las aplicaciones Android). En este caso en particular, la aplicación será <code>com.kivy.amicos_caa</code>.

- **source.dir**: directorio donde se encuentran los ficheros de código fuente, que generalmente serán aquellos que se encuentren en el mismo lugar que el propio buildozer.spec.

- **source.include_exts**: indica qué extensiones de ficheros se deben tener en cuenta. Este campo es muy importante cuando se añaden archivos de configuración o adicionales. Por ejemplo, los ficheros json que contienen las strings de los elementos de la UI se pueden incorporar a la compilación añadiendo "json" a esta línea. En otras palabras, si después de compilar se recibe el error "no se ha encontrado el fichero ruta/strings.json", probablemente se deba porque falta añadir json a esa línea. Lo mismo para cualquier otro tipo de archivo adicional.

- **version**: versión de la aplicación.

- **requirements**: esta es una de las partes de mayor relevancia. Si alguna de las dependencias falta aquí, la aplicación no se compilará. Cabe destacar que las dependencias que se pueden añadir aquí corresponden a las recipes del repositorio de GitHub de python-for-android. En otro caso, no se garantiza que Buildozer sea capaz de encontrar la librería.

- **icon.filename**: ruta del icono de la aplicación. Con una imagen de 512 x 512, el icono debería de poder visualizarse de forma correcta. 

- **android.permissions**: esta línea es muy importante cuando la aplicación requiere de permisos adicionales, por ejemplo de la cámara o del almacenamiento del dispositivo. Para que se puedan conceder los permisos de forma exitosa, primero tienen que especificarse los permisos que hacen falta aquí (ya que buildozer.spec funciona en cierta forma como un AndroidManifest y, por tanto, es necesario que el sistema operativo sepa qué permisos va a requerir la aplicación). A continuación, estos permisos deben pedirse de forma explícita desde el código. Si alguno de los permisos no está en ambas partes, no se concederá de manera satisfactoria y la aplicación dará error.

- **android.gradle_dependencies** y **android.add_gradle_repositories**: estas dos líneas son extremadamente importantes si se desea utilizar alguna librería externa nativa de Android que no se pueda acceder por defecto. Esto ocurre, por ejemplo, con la librería mediapipe, que no se puede utilizar directamente desde Python, ya que eso daría algunos problemas y que, si se trabajase con Java/Kotlin, sería necesario añadir la dependencia en Gradle. Para el caso particular de mediapipe facemesh, extrapolable a cualquier otra librería externa, habría que añadir **android.gradle_dependencies** como <code>com.google.mediapipe:facemesh:0.10.20</code> y **android.add_gradle_repositories** como <code>"maven {url 'https://mvnrepository.com/artifact/com.google.mediapipe/facemesh/0.10.20'}"</code>. En términos generales, para saber qué líneas se deben añadir, es necesario consultar la descripción en el repositorio de Maven.
