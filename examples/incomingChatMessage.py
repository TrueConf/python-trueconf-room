"""
Example: Receiving an incoming chat message
"""

import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
import config

print(__doc__)

room = trueconf_room.open_session(ip = config.IP, port = config.PORT, pin = config.PIN, debug = config.DEBUG)
methods = Methods(room)

@room.handler(EVENT[C.EV_appStateChanged])
@room.handler(METHOD_RESPONSE[C.M_getAppState])
def on_state_change(response):
    print(f'State changed to: {response["appState"]}')

@room.handler(EVENT[C.EV_incomingChatMessage])
def on_chat_massage(response):
    print('Incoming chat message')
    print(f'    From   : {response["peerId"]}')
    print(f'    Message: {response["message"]}')

if __name__ == '__main__':
    print(__doc__)
    room.run()