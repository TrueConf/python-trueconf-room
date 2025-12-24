"""
Example:
    Processing of the invite received.
"""

import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
import config

room = trueconf_room.open_session(ip = config.IP, port = config.PORT, pin = config.PIN, debug = config.DEBUG)
methods = Methods(room)

@room.handler(EVENT[C.EV_appStateChanged])
@room.handler(METHOD_RESPONSE[C.M_getAppState])
def on_state_change(response):
    print(f'    @@@ {response["appState"]}')

@room.handler(EVENT[C.EV_inviteReceived])
def on_invite(response):
    print('Incoming call:')
    print(f'             Type: {response["type"]}')
    print(f'             From: {response["peerId"]}')
    print(f'             Name: {response["peerDn"]}')
    print(f'    Conference ID: {response["confId"]}\n')
    # Ask
    if input("Accept incoming? (y/n): ").lower() == "y":
        # Accept
        methods.accept()
        print("Call accepted.")
    else:
        methods.reject()
        print("Call rejected.")

if __name__ == '__main__':
    room.run()