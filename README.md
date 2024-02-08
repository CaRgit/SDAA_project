# Proyecto de integración entre Raspberry Pi y altavoz SONOS
Este proyecto permite controlar un altavoz Sonos utilizando una Raspberry Pi. Se crea un servidor local para enviar mensajes HTTP al altavoz Sonos y gestionar su reproducción de forma remota. Además, se integra funcionalidad de detección de presencia utilizando la cámara de la Raspberry Pi mediante técnicas de machine learning.

# Características principales:
- **Control del altavoz Sonos**: Se establece una comunicación con el altavoz Sonos a través de mensajes HTTP para controlar su reproducción, volumen y otras funciones desde la Raspberry Pi.
- **Detección de presencia**: Se utiliza la cámara de la Raspberry Pi junto con algoritmos de machine learning para detectar la presencia de personas en el entorno y realizar ciertas acciones en función de ello.
-	**Interfaz con joystick**: Se detectan los eventos del joystick conectado a la Raspberry Pi para enviar señales adicionales al altavoz Sonos, como cambiar de pista o ajustar el volumen.
-	**Visualización de información**: Se utiliza el Sense HAT de la Raspberry Pi para mostrar información visual, proporcionando retroalimentación al usuario sobre el estado del sistema.

# Requisitos:
-	Raspberry Pi con Sense HAT y cámara compatible.
-	Altavoz Sonos compatible.
-	Conexión a internet para instalar dependencias y actualizar el software.
