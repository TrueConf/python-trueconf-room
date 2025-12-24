"""
Example:
  1. Connect to TrueConf Server.
  2. Log in user.
"""

import trueconf_room
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import trueconf_room.consts as C
import config

print(__doc__)

TRUECONF_SERVER = "<Server IP>"
TRUECONF_ID = "<trueconf_id>"
PASSWORD = "<password>"

room = trueconf_room.open_session(ip = config.IP, port = config.PORT, pin = config.PIN, debug = config.DEBUG)
methods = Methods(room)

@room.handler(EVENT[C.EV_appStateChanged])
def on_state_change(response):
    print(f'    Application state is {response["appState"]}')
    # Need to login
    if (response["appState"] == 2):
        methods.login(TRUECONF_ID, PASSWORD)

if __name__ == '__main__':
    # Try to connect to TrueConf Server
    methods.connectToServer(TRUECONF_SERVER)
    room.run()