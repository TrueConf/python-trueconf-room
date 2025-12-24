"""
Example:
    Fire a custom event through TrueConf Room

API Version: 4.1.0+

"""

import config
import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
from pprint import pprint

print(__doc__)

room = trueconf_room.open_session(ip = config.IP, port = config.PORT, pin = config.PIN, debug = config.DEBUG)
methods = Methods(room)

@room.handler(EVENT[C.EV_appStateChanged])
@room.handler(METHOD_RESPONSE[C.M_getAppState])
def on_state_change(response):
    print(f'    Application state is {response["appState"]}')

@room.handler(METHOD_RESPONSE[C.M_fireMyEvent])
def on_fire_my_event_result(response):
    print("    Method call result:")
    pprint(response)

@room.handler(EVENT[C.EV_myEvent])
def on_my_event(response):
    print("    Event:")
    pprint(response)

if __name__ == '__main__':
    methods.fireMyEvent("hello_world_event")
    room.run()