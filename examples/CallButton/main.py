import sys
import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import screeninfo

import wstyle

# ========================
# Configuration
# ========================
ROOM_IP: str = "127.0.0.1"
ROOM_PORT: int = 2233
PIN: str = "123"
MINMAX_APPLICATION: bool = True
CALL_ID: str = "echotest_es@trueconf.com"
# ========================

TITLE: str = "Button Video Calling Demo"
BUTTON_WIDTH: int = 160
BUTTON_HEIGHT: int = 90
INDENT: int = 100
MONITOR: int = 0
IMAGE_BUTTON: str = "call.png"
ICON_SIZE: int = 64

sdk = trueconf_room.open_session(ip=ROOM_IP, port=ROOM_PORT, pin=PIN, debug=False)
methods = Methods(sdk)


class KioskButton(QWidget):
    def __init__(self, monitor: int):
        super().__init__()

        self.layout = None
        self.room = None
        self.displayName = ""
        self.buttonCall = None
        self.buttonCallTag = False
        if monitor >= len(screeninfo.get_monitors()) or monitor < 0:
            monitor = 0
        self.monitor = screeninfo.get_monitors()[monitor]
        self.state = 0
        self.initUI()

    def initUI(self):
        # Setting layout
        self.layout = QVBoxLayout(self)
        # Position
        self.setPosition()

        self.setWindowTitle(TITLE)
        # Frameless window
        self.setWindowFlags(Qt.WindowStaysOnTopHint
                            | Qt.X11BypassWindowManagerHint | Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Show
        self.show()
        # connectToRoom
        self.connectToRoom()
        # Button
        self.buttonCall = self.createCallButton(
            style=wstyle.STYLE_GRAY_BUTTON, icon=IMAGE_BUTTON)
        # flashing timer
        self.timer = QTimer(self, interval=500)
        self.timer.timeout.connect(self.flashing)
        self.timer.start()

    def createCallButton(self, style: str, icon: str) -> object:
        button = QPushButton()
        button.setStyleSheet(style)
        button.setFixedWidth(BUTTON_WIDTH)
        button.setFixedHeight(BUTTON_HEIGHT)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(button)
        self.layout.setAlignment(button, Qt.AlignRight | Qt.AlignBottom)

        if icon:
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

        button.clicked.connect(self.on_click_call)
        return button

    def setPosition(self):
        # calc window size & position
        leftCoord: int = self.monitor.x + self.monitor.width - BUTTON_WIDTH - INDENT
        topCoord: int = self.monitor.y + self.monitor.height - BUTTON_HEIGHT - INDENT

        # set position
        self.setGeometry(leftCoord, topCoord, BUTTON_WIDTH, BUTTON_HEIGHT)

    def flashing(self):
        if self.state == 3:
            if self.buttonCallTag:
                self.buttonCall.setStyleSheet(wstyle.STYLE_GREEN_BUTTON_FLASH)
            else:
                self.buttonCall.setStyleSheet(wstyle.STYLE_GREEN_BUTTON)

        self.buttonCallTag = not self.buttonCallTag

    def connectToRoom(self):
        pass

    def on_state_change(self, response):
        # Get the current state
        self.state = response["appState"]

        # Set button color according to status
        if self.state == 3:
            style = wstyle.STYLE_GREEN_BUTTON
        elif self.state in [4, 5]:
            style = wstyle.STYLE_RED_BUTTON
        else:
            style = wstyle.STYLE_GRAY_BUTTON
        self.buttonCall.setStyleSheet(style)

        if MINMAX_APPLICATION:
            if self.state in [4, 5]:
                methods.showMainWindow(True, False)  # Maximized
            else:
                methods.showMainWindow(False)  # Minimized, Hiden

    @pyqtSlot()
    def on_click_call(self):
        self.displayName = self.sender().text
        if self.state == 3:
            # Calling
            methods.call(CALL_ID)
        elif self.state in [4, 5]:
            # Hang up
            methods.hangUp(True)
        else:
            print("Warning. Please check connection.")


@sdk.handler(EVENT[C.EV_rejectReceived])
def on_reject_received(response):
    print(C.CAUSE[response["cause"]])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    call_button = KioskButton(MONITOR)

    # Add handlers
    sdk.add_handler(EVENT[C.EV_appStateChanged], call_button.on_state_change)
    sdk.add_handler(METHOD_RESPONSE[C.M_getAppState],
                    call_button.on_state_change)
    # Request the current state
    methods.getAppState()

    sys.exit(app.exec_())
