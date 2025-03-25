# Mp3 Player

## Descripción

Un reproductor de música simulado desarrollado en **Python**. La aplicación utiliza **Tkinter** para la interfaz gráfica y **Pillow (PIL)** para el manejo y redimensionamiento de imágenes. La lógica central se basa en una implementación personalizada de una **lista doblemente enlazada**, que gestiona dinámicamente la playlist de canciones.

## Tecnologías y Herramientas

- **Lenguaje:** Python 3.x
- **Interfaz Gráfica:** Tkinter (incluido en la biblioteca estándar de Python)
- **Librerías:**
  - [Pillow (PIL)](https://python-pillow.org/) – para cargar y redimensionar imágenes.
  - **os** – para gestionar rutas y directorios (por ejemplo, para obtener la ruta actual y construir la ruta a la carpeta de imágenes).

## Estructura del Proyecto


## Funcionalidades

- **Playlist Dinámica con Lista Doblemente Enlazada:**  
  - Cada nodo almacena la información de una canción en su atributo `data`.
  - Cada nodo tiene dos punteros: `prev` (hacia el nodo anterior) y `next` (hacia el nodo siguiente), lo que permite recorrer la lista en ambas direcciones.
  - Métodos para insertar, eliminar y reordenar canciones (incluyendo mover nodos a la cabeza o intercambiar datos entre nodos adyacentes).

- **Interfaz del Reproductor:**  
  - **Panel Izquierdo:** Muestra la portada, título, artista, álbum y una barra de progreso interactiva.
  - **Panel Derecho:** Muestra la lista de canciones con controles para seleccionar, reordenar y eliminar ítems.
  - Se muestran mensajes en consola para acciones clave (selección, navegación, mute, play/pause, etc.), lo que facilita la depuración.

## Uso del Módulo os

El módulo `os` se utiliza para:
- Obtener el directorio actual con `os.getcwd()`.
- Determinar la ruta base del proyecto y construir la ruta a la carpeta `img` con `os.path.dirname(os.path.abspath(__file__))` y `os.path.join(...)`.
  
Esto asegura que los recursos gráficos se carguen correctamente en cualquier entorno.

## Cómo Ejecutar el Proyecto

1. **Clonar el Repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/proyecto_mp3_player.git
   cd proyecto_mp3_player
