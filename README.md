<p align="center">
  <a href="https://trueconf.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/TrueConf/.github/refs/heads/main/logos/logo-dark.svg">
      <img width="150" alt="trueconf" src="https://raw.githubusercontent.com/TrueConf/.github/refs/heads/main/logos/logo.svg">
    </picture>
  </a>
</p>

<h1 align="center">python-trueconf-room</h1>

<p align="center">Python library for the TrueConf Room API</p>

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
  <a href="https://github.com/TrueConf/python-trueconf-room/blob/master/README.md">English</a> /
  <a href="https://github.com/TrueConf/python-trueconf-room/blob/master/README-ru.md">Русский</a> /
  <a href="https://github.com/TrueConf/python-trueconf-room/blob/master/README-de.md">Deutsch</a> /
  <a href="https://github.com/TrueConf/python-trueconf-room/blob/master/README-es.md">Español</a>
</p>

**TrueConf Room** — a software terminal for meeting rooms and conference halls of any size. It is installed on PCs running Windows or Linux OS, and provides a convenient control interface via a web interface or smartphone and tablet application based on Android. For more details, see the [documentation for TrueConf Room](https://trueconf.com/docs/videosdk/en/introduction/common).

> [!NOTE]
> This library currently supports **API v1 only**. Support for **API v2** will be added in a future update.

## 🚀 How to use `python-trueconf-room`

1. Download and install **TrueConf Room** using the [direct link](https://github.com/TrueConf/python-trueconf-room/blob/master/download_links.md).

2. Launch TrueConf Room with the [`--pin`](https://trueconf.ru/docs/videosdk/ru/introduction/commandline#pin) parameter:

   **Windows:**

   ```sh
   "C:\Program Files\TrueConf\Room\TrueConfRoom.exe" --pin some_pin
   ```

   **Linux:**

   ```sh
   trueconf-room --pin some_pin
   ```

3. You can now connect to TrueConf Room using the following example:

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

## 🧩 Library overview

**python-trueconf-room** is a Python library for controlling **TrueConf Room** via the **TrueConf Room API**. Communication is organized around a “command → response” workflow, plus **events** that are delivered automatically when the application state changes. Data is exchanged over **WebSocket** in **JSON** format, but you don’t need to manually assemble or parse JSON payloads—the library handles that for you.

### 📦 Module imports

In most cases, four imports are sufficient:

```python
import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
```

* `trueconf_room` is the main module. It is used to create a session (`open_session`), register handlers (`handler`), and start the incoming message loop (`run`).
* `Methods` is a class that exposes TrueConf Room API commands as Python methods. It provides a convenient abstraction that lets you call commands by name without manually preparing requests.
* `EVENT` and `METHOD_RESPONSE` are input notification types used when registering handlers:

  * `EVENT` — asynchronous events (e.g., incoming call, application state change, etc.),
  * `METHOD_RESPONSE` — responses to commands you invoked via `methods`.
* `import trueconf_room.consts as C` imports all constants under the short alias `C`. This keeps the code readable: instead of long constant paths, you write `C.EV_...` and `C.M_...`, making it immediately clear that these are API event or method identifiers.

### 🔌 Creating a session and objects

Work begins by creating the `room` object. This is an active session that maintains a connection to TrueConf Room and receives all incoming messages:

```py
room = trueconf_room.open_session(ip="127.0.0.1", port=80, pin="some_pin")
```

Next, create the `methods` object. It uses the existing `room` session to send commands to the TrueConf Room API:

```py
methods = Methods(room)
```

### 🪝 Handlers

TrueConf Room continuously sends notifications—either responses to your commands or events that occur independently. To avoid manually processing the entire stream, the library provides **handlers**.

A **handler** is a regular function that the library calls automatically when a matching event or response arrives. Handlers are registered via the `@room.handler(...)` decorator.

Key rules:

* For events, use `EVENT[...]` with `C.EV_...` constants.
* For command responses, use `METHOD_RESPONSE[...]` with `C.M_...` constants.

Example: handling an application state change and an incoming call:

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
> A handler function always takes a single `response` argument—this is already-parsed JSON represented as a Python dictionary.

## ⚡️ Calling commands

Commands are invoked through the `methods` object. Method names match the original TrueConf Room API command names, so mapping from the documentation is straightforward: find a command in the API docs and call the method with the same name in `Methods`.

Example command call:

```py
methods.getHardware()
```

The response will arrive as a separate notification. To process it, register a handler for `METHOD_RESPONSE[C.M_getHardware]`.

### 🏃‍♂️ Starting the message loop

After registering handlers and (optionally) sending initial commands, start the processing loop:

```py
room.run()
```

`run()` keeps the session active and allows the library to receive responses and events until the connection is closed.

## 📚 Documentation

1. [TrueConf Room API documentation](https://trueconf.ru/docs/videosdk/ru/introduction/common)
2. [Code examples](https://github.com/TrueConf/python-trueconf-room/blob/master/examples/):

   1. [General examples](https://github.com/TrueConf/python-trueconf-room/blob/master/examples/)
   2. [Call button using PyQt5](https://github.com/TrueConf/python-trueconf-room/blob/master/examples/CallButton/)
   3. [TrueConf Room voice control with Vosk](https://github.com/TrueConf/pyVideoSDK-VoiceControl)
