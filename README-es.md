<p align="center">
  <a href="https://trueconf.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/TrueConf/.github/refs/heads/main/logos/logo-dark.svg">
      <img width="150" alt="trueconf" src="https://raw.githubusercontent.com/TrueConf/.github/refs/heads/main/logos/logo.svg">
    </picture>
  </a>
</p>

<h1 align="center">python-trueconf-room</h1>

<p align="center">Biblioteca de Python para la API de TrueConf Room</p>

<p align="center">
    <a href="https://pypi.org/project/python-trueconf-room/">
        <img src="https://img.shields.io/pypi/v/python-trueconf-room">
    </a>
    <a href="https://pypi.org/project/python-trueconf-room/">
        <img src="https://img.shields.io/pypi/pyversions/python-trueconf-room">
    </a>
    <a href="https://t.me/trueconf_chat" target="_blank">
        <img src="https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white" />
    </a>
    <a href="https://discord.gg/2gJ4VUqATZ">
        <img src="https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white" />
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/stars/trueconf/python-trueconf-room?style=social" />
    </a>
</p>

<p align="center">
  <a href="./README.md">English</a> /
  <a href="./README-ru.md">Русский</a> /
  <a href="./README-de.md">Deutsch</a> /
  <a href="./README-es.md">Español</a>
</p>

**TrueConf Room** es un terminal de software para salas de reuniones y salas de conferencias de cualquier tamaño.
Se instala en PCs con Windows o Linux y ofrece una interfaz de control cómoda mediante una interfaz web o una aplicación para smartphones y tabletas basada en Android.
Para más información, consulte la [documentación de TrueConf Room](https://trueconf.ru/docs/room/ru/introduction/).

> [!NOTE]
> Esta biblioteca actualmente solo admite la **API v1**. En una futura actualización se añadirá soporte para la **API v2**.

## 🚀 Cómo usar `python-trueconf-room`

1. Descargue e instale TrueConf Room desde el [enlace directo](https://raw.githubusercontent.com/TrueConf/python-trueconf-room/refs/heads/main/download_links.md).

2. Inicie TrueConf Room con el parámetro [`--pin`](https://trueconf.ru/docs/videosdk/ru/introduction/commandline#pin):

   **Windows:**

   ```sh
   "C:\Program Files\TrueConf\Room\TrueConfRoom.exe" --pin some_pin
   ```

   **Linux:**

   ```sh
   trueconf-room --pin some_pin
   ```

3. Ahora puede conectarse a TrueConf Room usando el siguiente ejemplo:

   ```py
   import trueconf_room
   from trueconf_room.methods import Methods
   from trueconf_room.consts import EVENT, METHOD_RESPONSE
   import trueconf_room.consts as C

   room = trueconf_room.open_session(ip = "127.0.0.1", port = 80, pin = "some_pin")
   methods = Methods(room)

   @room.handler(EVENT[C.EV_appStateChanged])
   def on_state_change(response):
       print(f'    Application state is {response["appState"]}')
       # Need to login
       if (response["appState"] == 2):
           methods.login("john_doe@video.example.com", "my_very_strong_password")

   if __name__ == '__main__':
   # Try to connect to TrueConf Server
   methods.connectToServer("video.example.com")
   room.run()
   ```

## 🧩 Descripción de la biblioteca

**python-trueconf-room** es una biblioteca de Python para controlar **TrueConf Room** a través de la **API de TrueConf Room**. La interacción se basa en el esquema «comando → respuesta», además de eventos que se envían automáticamente cuando cambia el estado de la aplicación. El intercambio de datos se realiza mediante **WebSocket** en formato **JSON**, pero el usuario no necesita construir ni analizar manualmente los paquetes JSON: la biblioteca lo hace por usted.

### 📦 Importación de módulos

Para un funcionamiento correcto, normalmente bastan cuatro importaciones:

```python
import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
```

`trueconf_room` es el módulo principal. A través de él se crea una sesión (`open_session`), se registran los manejadores (`handler`) y se inicia el bucle de procesamiento de mensajes entrantes (`run`).

`Methods` es una clase en la que los comandos de la API de TrueConf Room se presentan como métodos de Python. Es una capa práctica que permite invocar comandos «por nombre» sin preparar manualmente las solicitudes.

`EVENT` y `METHOD_RESPONSE` son tipos de notificaciones entrantes que se utilizan al registrar manejadores:

* `EVENT`: eventos (por ejemplo, llamada entrante, cambio del estado de la aplicación, etc.),
* `METHOD_RESPONSE`: respuestas a los comandos que ha invocado mediante `methods`.

`import trueconf_room.consts as C` importa todas las constantes con el alias corto `C`. Esto simplifica el código: en lugar de referencias largas, se escribe `C.EV_...` y `C.M_...`, y queda claro que se trata del nombre de un evento o un comando de la API.

### 🔌 Creación de la sesión y de los objetos

El trabajo comienza creando el objeto `room`. Es una sesión activa que mantiene la conexión con TrueConf Room y recibe todos los mensajes entrantes:

```py
room = trueconf_room.open_session(ip="127.0.0.1", port=80, pin="some_pin")
```

A continuación se crea el objeto `methods`. Utiliza la sesión `room` ya creada y, a través de ella, envía comandos a la API de TrueConf Room:

```py
methods = Methods(room)
```

### 🪝 Manejadores (handlers)

TrueConf Room envía notificaciones constantemente: pueden ser respuestas a sus comandos o eventos que ocurren por sí solos. Para no «capturar» manualmente todo el flujo de mensajes, la biblioteca utiliza manejadores.

Un **manejador** es una función normal que la biblioteca llama automáticamente cuando llega el evento o la respuesta correspondiente. Un manejador se registra mediante el decorador `@room.handler(...)`.

El principio clave es el siguiente:

* para eventos se utiliza `EVENT[...]` y las constantes `C.EV_...`;
* para respuestas a comandos se utiliza `METHOD_RESPONSE[...]` y las constantes `C.M_...`.

Ejemplo: manejo del cambio de estado de la aplicación y de una llamada entrante:

```py
@room.handler(EVENT[C.EV_appStateChanged])
@room.handler(METHOD_RESPONSE[C.M_getAppState])
def on_state_change(response):
    print(response["appState"])

@room.handler(EVENT[C.EV_inviteReceived])
def on_invite(response):
    print("Incoming call from:", response["peerId"])
    methods.accept()
```

> [!NOTE]
> Tenga en cuenta que una función manejadora siempre recibe un único parámetro `response`: es el JSON ya analizado en forma de diccionario de Python.

## ⚡️ Llamada de comandos

Los comandos se invocan mediante el objeto `methods`. Los nombres de los métodos coinciden con los nombres de los comandos en la API original de TrueConf Room, por lo que orientarse por la documentación es sencillo: encuentre el comando en la API y llame al método con el mismo nombre en `Methods`.

Ejemplo de llamada a un comando:

```py
methods.getHardware()
```

La respuesta a este comando llegará como una notificación independiente, y para procesarla es necesario registrar un manejador para `METHOD_RESPONSE[C.M_getHardware]`.

### 🏃‍♂️ Inicio del procesamiento de mensajes

Después de registrar los manejadores necesarios y (si es necesario) ejecutar los primeros comandos, debe iniciar el bucle de procesamiento:

```py
room.run()
```

`run()` mantiene la sesión activa y permite a la biblioteca recibir respuestas y eventos hasta que se cierre la conexión.

## 📚 Documentación

1. [Documentación de la API de TrueConf Room](https://trueconf.ru/docs/videosdk/ru/introduction/common)
2. [Ejemplos de código](examples/):

   1. [Ejemplos generales](examples/)
   2. [Botón de llamada con PyQt5](examples/CallButton/)
   3. [Control por voz de TrueConf Room con Vosk](https://github.com/TrueConf/trueconf-room-voice-control)
