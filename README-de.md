<p align="center">
  <a href="https://trueconf.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/TrueConf/.github/refs/heads/main/logos/logo-dark.svg">
      <img width="150" alt="trueconf" src="https://raw.githubusercontent.com/TrueConf/.github/refs/heads/main/logos/logo.svg">
    </picture>
  </a>
</p>

<h1 align="center">python-trueconf-room</h1>

<p align="center">Python-Bibliothek für die TrueConf Room API</p>

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

**TrueConf Room** ist ein Software-Terminal für Besprechungsräume und Konferenzsäle jeder Größe. Es wird auf PCs mit Windows oder Linux installiert und bietet eine komfortable Steuerung über eine Weboberfläche oder eine App für Smartphones und Tablets auf Android-Basis. Weitere Informationen finden Sie in der [Dokumentation zu TrueConf Room](https://trueconf.com/docs/videosdk/en/introduction/common).

> [!NOTE]
> Diese Bibliothek unterstützt derzeit ausschließlich **API v1**. Die Unterstützung für **API v2** wird in einem zukünftigen Update ergänzt.

## 🚀 Verwendung von `python-trueconf-room`

1. Laden Sie **TrueConf Room** über den [Direktlink](https://raw.githubusercontent.com/TrueConf/python-trueconf-room/refs/heads/main/download_links.md) herunter und installieren Sie es.

2. Starten Sie TrueConf Room mit dem Parameter [`--pin`](https://trueconf.ru/docs/videosdk/ru/introduction/commandline#pin):

   **Windows:**

   ```sh
   "C:\Program Files\TrueConf\Room\TrueConfRoom.exe" --pin some_pin
   ```

   **Linux:**

   ```sh
   trueconf-room --pin some_pin
   ```

3. Anschließend können Sie sich mit TrueConf Room anhand des folgenden Beispiels verbinden:

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

## 🧩 Bibliotheksbeschreibung

**python-trueconf-room** ist eine Python-Bibliothek zur Steuerung von **TrueConf Room** über die **TrueConf Room API**. Die Kommunikation folgt dem Muster „Befehl → Antwort“ und nutzt zusätzlich **Ereignisse (Events)**, die bei Zustandsänderungen der Anwendung automatisch gesendet werden. Der Datenaustausch erfolgt über **WebSocket** im **JSON**-Format. Dabei müssen Nutzer jedoch keine JSON-Pakete manuell erstellen oder auswerten – das übernimmt die Bibliothek.

### 📦 Modulimporte

Für den korrekten Betrieb reichen in der Regel vier Imports aus:

```python
import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
```

`trueconf_room` — das Hauptmodul. Darüber wird eine Session erstellt (`open_session`), Handler werden registriert (`handler`) und der Verarbeitungslauf für eingehende Nachrichten gestartet (`run`).

`Methods` — eine Klasse, in der die Befehle der TrueConf Room API als Python-Methoden abgebildet sind. Sie bietet eine komfortable Abstraktionsschicht, um Befehle „per Namen“ aufzurufen, ohne Requests manuell vorbereiten zu müssen.

`EVENT` und `METHOD_RESPONSE` — Typen eingehender Benachrichtigungen, die bei der Registrierung von Handlern verwendet werden:

* `EVENT` — asynchrone Ereignisse (z. B. eingehender Anruf, Änderung des Anwendungszustands usw.),
* `METHOD_RESPONSE` — Antworten auf Befehle, die Sie über `methods` ausgelöst haben.

`import trueconf_room.consts as C` — importiert alle Konstanten unter dem kurzen Alias `C`. Das macht den Code übersichtlicher: Statt langer Verweise schreiben Sie `C.EV_...` und `C.M_...` – und es ist sofort klar, dass es sich um Event- bzw. Methodenbezeichner aus der API handelt.

### 🔌 Session und Objekte erstellen

Die Arbeit beginnt mit der Erstellung des Objekts `room`. Das ist eine aktive Session, die die Verbindung zu TrueConf Room hält und alle eingehenden Nachrichten empfängt:

```py
room = trueconf_room.open_session(ip="127.0.0.1", port=80, pin="some_pin")
```

Anschließend wird das Objekt `methods` erzeugt. Es nutzt die bereits erstellte Session `room` und sendet darüber Befehle an die TrueConf Room API:

```py
methods = Methods(room)
```

### 🪝 Handler

TrueConf Room sendet fortlaufend Benachrichtigungen – entweder Antworten auf Ihre Befehle oder Ereignisse, die unabhängig von Ihren Aktionen auftreten. Damit Sie nicht den gesamten Nachrichtenstrom manuell verarbeiten müssen, stellt die Bibliothek **Handler** (Ereignis- und Response-Handler) bereit.

Ein **Handler** ist eine normale Funktion, die von der Bibliothek automatisch aufgerufen wird, sobald das passende Ereignis oder die passende Antwort eintrifft. Registriert wird ein Handler über den Dekorator `@room.handler(...)`.

Grundprinzip:

* Für Events verwenden Sie `EVENT[...]` in Kombination mit Konstanten `C.EV_...`.
* Für Antworten auf Befehle verwenden Sie `METHOD_RESPONSE[...]` in Kombination mit Konstanten `C.M_...`.

Beispiel: Verarbeitung einer Zustandsänderung der Anwendung und eines eingehenden Anrufs:

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
> Beachten Sie: Eine Handler-Funktion erhält immer genau einen Parameter `response` – das ist bereits geparstes JSON in Form eines Python-Dictionaries.

## ⚡️ Befehle aufrufen

Befehle werden über das Objekt `methods` aufgerufen. Die Methodennamen entsprechen den Befehlsnamen der originalen TrueConf Room API. Dadurch ist die Orientierung in der Dokumentation einfach: Finden Sie einen Befehl in der API-Doku, rufen Sie die gleichnamige Methode in `Methods` auf.

Beispiel für einen Befehlsaufruf:

```py
methods.getHardware()
```

Die Antwort auf diesen Befehl wird als separate Benachrichtigung gesendet. Um sie zu verarbeiten, registrieren Sie einen Handler für `METHOD_RESPONSE[C.M_getHardware]`.

### 🏃‍♂️ Verarbeitungsschleife starten

Nachdem Sie die gewünschten Handler registriert und (falls erforderlich) erste Befehle ausgelöst haben, starten Sie die Verarbeitungsschleife:

```py
room.run()
```

`run()` hält die Session aktiv und ermöglicht der Bibliothek, Antworten und Events zu empfangen, bis die Verbindung geschlossen wird.

## 📚 Dokumentation

1. [TrueConf Room API-Dokumentation](https://trueconf.com/docs/videosdk/en/introduction/common)
2. [Codebeispiele](https://github.com/TrueConf/python-trueconf-room/blob/main/examples/):

   1. [Allgemeine Beispiele](https://github.com/TrueConf/python-trueconf-room/blob/main/examples/)
   2. [Anruf-Button mit PyQt5](https://github.com/TrueConf/python-trueconf-room/blob/main/examples/CallButton/)
   3. [Sprachsteuerung von TrueConf Room mit Vosk](https://github.com/TrueConf/pyVideoSDK-VoiceControl)
