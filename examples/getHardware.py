"""
Example:
    1. Get a list of the hardware.
    2. Close the session.
"""
from pprint import pprint
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

@room.handler(METHOD_RESPONSE[C.M_getHardware])
def on_get_hardware(response):
    print('==============================================')
    print('Hadrware list:')
    print('==============================================')
    pprint(response)
    print('==============================================')
    # Close the session
    room.close_session()

if __name__ == '__main__':
    methods.getHardware()
    room.run()